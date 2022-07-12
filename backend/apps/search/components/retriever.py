from typing import Dict, List, Union

from .db_connector import DBIndex
from .es_connector import ESIndex
from .reader import Reader
from .ranker import Reranker
from .inferrer import Inferrer

class Retriever:
    """Get API connecting multiple backend components to accomplish
    relevant answer & document retrieval task."""

    def __init__(
        self,
        db_setting: Dict[str, Union[str, int]],
        es_setting: Dict[str, Union[str, int]],
        reranker_setting: Dict[str, int],
        reader_setting: Dict[str, Union[str, int]],
        inferrer_setting: Dict[str, Union[str, int]],
    ) -> None:
        self.db_conn = DBIndex(**db_setting)
        self.es_conn = ESIndex(**es_setting)
        self.reader_conn = Reader(**reader_setting)
        self.reranker_conn = Reranker(**reranker_setting)
        self.inferrer_conn = Inferrer(**inferrer_setting)

    def get_document_by_id(
        self,
        docs: List[Dict[str, str]],
        doc_id: int,
    ) -> Dict[str, str]:
        """Return document by the given document's ID.

            Args:
                docs (List[Dict[str, str]]): list of retrieve documents from text-based method
                doc_id (int): target document's id

            Returns:
                dict: target document containing the answer
        """
        for doc in docs:
            if doc_id == int(doc["id"]):
                return doc

        return None

    def retrieve(self, query: str) -> Dict[str, Union[Dict, List]]:
        """Conduct retrieval-rerank based on the given query 

        Args:
            query (str): user query

        Returns:
            Dict[str, Union[Dict, List]]: results of both full-text search
            and after re-ranking.
                Format:
                {
                    "full-text": list of documents with relevant information,
                    "re-rank": list of ranked sentences by semantic search method,   
                }
        """
        # Step 2, 3
        docs = self.es_conn.retrieve_documents(query)   # 0-index

        # Get list of relevant documents' IDs
        # Convert IDs from 0-index to 1-index to query database
        doc_ids = list(map(lambda entry: int(entry.get("id"))+1, docs["docs"])) # 1-index

        # Step 4, 5
        list_sent_ids = self.db_conn.get_sentences_ids(doc_ids)     # 1-index
        # Convert the IDs from 1-index back to 0-index to work with faiss index
        list_sent_ids = [(_id-1) for _id in list_sent_ids]  # 0-index

        # Step 6, 7, 8, 9, 10
        ranked_sentences = self.reranker_conn.rerank(list_sent_ids, query)  # 0-index
        # Extract IDs from ranked sentences
        ranked_sentence_ids = [sent["id"] for sent in ranked_sentences]     # 0-index
        ranked_scores = {sent["id"]: sent["distance"] for sent in ranked_sentences}

        # Convert the IDs from 0-index back to 1-index to work with the database
        ranked_sentence_ids = [(id_+1) for id_ in ranked_sentence_ids]  # 1-index

        # Step 11, 12
        sentences = self.db_conn.retrieve_sentences(ranked_sentence_ids)    # 1-index

        counting_arr = []
        # Get corresponding documents selected from re-ranking stage
        reranked_docs = []
        for sent_id in sentences.keys():
            doc_id = self.db_conn.get_doc_id(sent_id=sent_id)
            # Avoid duplicate in 
            if doc_id in counting_arr:
                continue
            counting_arr.append(doc_id)

            # Convert the IDs from 1-index back to 0-index to work with ES results
            doc = self.get_document_by_id(
                docs=docs["docs"],  # 0-index
                doc_id=doc_id-1,    # 0-index
            )

            # Re-name the text-score
            text_score = doc["score"]
            doc.pop("score", None)
            doc["text_score"] = text_score
            # Add the semantic-score
            doc["semantic_score"] = ranked_scores[sent_id-1]    # 1-index -> 0-index
            reranked_docs.append(doc)

        results = {
            "full-text": docs,
            "re-ranking": {
                "documents": reranked_docs,
                "sentences": sentences,
            },
        }
        return results

    def retrieve_answer(self, query: str) -> Dict:
        """Retrieve and extract answer from indexes for the given question query

        Args:
            query (str): user's query

        Returns:
            Dict: combination of extracted answer and relevant data
                Format:
                {
                    "query": <str>,
                    "answer": <str>
                }
        """
        # Step 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        retrieval_result = self.retrieve(query)
        sentences = retrieval_result["re-ranking"]["sentences"]

        # Step 13, 14, 15, 16
        result = self.reader_conn.get_answer(sentences, query)  # 1-index
        answer = result.get("answer")
        answer_score = result.get("score")
        # Retrieve corresponding document
        sent_id = result.get("sent_id")[0]      # 1-index

        # Retrieve the associated document (additional feature)
        # sent_id which is received from the database is already 1-index,
        # hence we don't need to increment it to solve index mismatching
        doc_id = self.db_conn.get_doc_id(sent_id)   # 1-index

        # Convert the IDs from 1-index back to 0-index to work with ES results
        selected_document = self.get_document_by_id(
            docs=retrieval_result["re-ranking"]["documents"],  # 0-index
            doc_id=doc_id-1,    # 0-index
        )

        return {
            "query": query,
            "answer": answer,
            "answer_score": answer_score,
            "document": {**selected_document},
        }

    def retrieve_inference(self, query: str) -> Dict:
        """Retrieve inference for the given query (premise) based on hypothesis
        of the data the system has.

        Args:
            query (str): user query (premise)

        Returns:
            Dict: list of retrieved data with inference result. The format is
            similar to the inference result from the Inferrer with additional 
            information about the context containing the hypothesis.
                Format:
                {
                    "insight": {
                        ...
                    },
                    "data": [
                        {
                            ...
                            "context": {
                                "content": <str>,
                                "id": <int>,
                                "semantic_score": <float>,
                                "text_score": <float>
                            },
                        }
                    ]
                }
        """
        retrieval_result = self.retrieve(query)
        docs = retrieval_result["full-text"]
        sentences = retrieval_result["re-ranking"]["sentences"]
      
        infer_result = self.inferrer_conn.get_inference(
            query=query,    
            sentences=sentences,
        )

        for res in infer_result["data"]:
            doc_id = self.db_conn.get_doc_id(res["sent_id"])    # 1-index
            # Convert the IDs from 1-index back to 0-index to work with ES results
            doc = self.get_document_by_id(
                docs=docs["docs"],  # 0-index
                doc_id=doc_id-1,    # 0-index
            )

            res["context"] = doc 

        return infer_result


    def __str__(self) -> str:
        return """
            MySQL: {!s}
            ElasticSearch: {!s}
            Reranker: {!s}
            Reader: {!s}
            Inferrer: {!s}
        """.format(
            self.db_conn,
            self.es_conn,
            self.reranker_conn,
            self.reader_conn,
            self.inferrer_conn,
        )

    def __repr__(self) -> str:
        return """
            MySQL: {!r}
            ElasticSearch: {!r}
            Reranker: {!r}
            Reader: {!r}
            Inferrer: {!r}
        """.format(
            self.db_conn,
            self.es_conn,
            self.reranker_conn,
            self.reader_conn,
            self.inferrer_conn,
        )
