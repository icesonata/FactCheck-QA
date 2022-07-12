from typing import Dict, List, Union

from elasticsearch import Elasticsearch


class ESIndex:
    """Control over ElasticSearch index to conduct specific tasks."""

    # ElasticSearch reserved characters
    ESCAPE_RULES = {
        '+': r'\+',
        '-': r'\-',
        '&': r'\&',
        '|': r'\|',
        '!': r'\!',
        '(': r'\(',
        ')': r'\)',
        '{': r'\{',
        '}': r'\}',
        '[': r'\[',
        ']': r'\]',
        '^': r'\^',
        '~': r'\~',
        '*': r'\*',
        '?': r'\?',
        ':': r'\:',
        '"': r'\"',
        '\\': r'\\;',
        '/': r'\/',
        '>': r' ',
        '<': r' ',
    }

    def __init__(
        self,
        host: str,
        port: int,
        index: str,
        list_fields: List[str],
        K: int = 100,
    ) -> None:
        self._config = {
            "host": host,
            "port": port,
            "index": index,
        }
        self.conn = Elasticsearch(
            [
                {
                    "host": self._config["host"],
                    "port": self._config["port"],
                }
            ],
        )
        self._list_fields = list_fields
        self.K = K

    def escapedSeq(self, term: str) -> str:
        """ Yield the next string based on the
            next character (either this char
            or escaped version.

            Args:
            - term: raw term

            Returns:
            - str: processed query's term
        """
        for char in term:
            if char in self.ESCAPE_RULES.keys():
                yield self.ESCAPE_RULES[char]
            else:
                yield char

    def escapeESArg(self, term: str) -> str:
        """ ElasticSearch preprocess:
            Apply escaping to the passed in query terms
            escaping special characters like : , etc.

            Args:
            - term: raw term

            Returns:
            - str: escaped term
        """
        # Source: https://stackoverflow.com/a/53552181/11806074
        term = term.replace('\\', r'\\')   # escape \ first
        return "".join([nextStr for nextStr in self.escapedSeq(term)])

    def normalize_scores(
        self,
        list_docs: List[Dict],
    ) -> List[Dict[str, Union[str, float]]]:
        """Apply min-max normalization to scores to rescale to [0,1] range.

            Args:
                list_docs (List[Dict]): list of dictionaries containing scores.
                    Format:
                    [
                        {
                            "id": <str>,
                            "title": <str>,
                            "content": <str>,
                            "score": <float>
                        },
                        ...
                    ]

            Returns:
                list: original list of dictionaries with normalized scores
        """
        list_scrs = list(map(lambda doc: doc.get("score"), list_docs))
        max_scr = max(list_scrs)
        min_scr = min(list_scrs)
        denominator = max_scr - min_scr
        for idx, scr in enumerate(list_scrs):
            normalized = (scr - min_scr) / denominator
            list_docs[idx]["score"] = normalized
        return list_docs

    def preprocess(self, usr_query: str) -> str:
        """Preprocess user query

        Args:
            usr_query (str): user query

        Returns:
            str: processed user query
        """
        processed_query = self.escapeESArg(usr_query)
        return processed_query

    # Step 2, 3

    def retrieve_documents(
        self,
        query: str,
    ) -> List[Dict[str, Union[str, float, Dict[str, Union[float, str, int]]]]]:
        """Return relevant documents from text-based method.

            Args:
            - query: user's query
            - list_fields: retrieve entries based on matching the given fields 

            Returns:
            - list: list of documents retrieved using text-based method
                {
                    "count": <int>,
                    "max_score": <float>,
                    "min_score": <float,
                    "docs": [
                        {
                            "id": <str>,
                            "score": <float>,       // normalized

                            (list of given fields, mapping "<field>": "<dtype">)
                        },
                        ...
                    ]
                }
        """
        # Preprocess input data
        query = self.preprocess(query)

        # Searching
        response = self.conn.search(index=self._config["index"], body={
            "query": {
                "query_string": {
                    "query": query,
                    "fields": self._list_fields,
                    "default_operator": "OR",
                }
            }
        }, size=self.K, request_timeout=200)

        matched_doc = []
        for hit in response["hits"]["hits"]:
            doc = {
                "id": hit["_id"],
                "score": hit["_score"],
            }
            for field in self._list_fields:
                try:
                    doc[field] = hit["_source"]["doc"][field]
                except KeyError:
                    doc[field] = hit["_source"][field]
            matched_doc.append(doc)

        # Assume retrieved documents from ElasticSearch are in descending by score
        max_score = matched_doc[0]["score"]
        min_score = matched_doc[-1]["score"]
        count = len(matched_doc)

        # Apply normalization to scores
        matched_doc = self.normalize_scores(matched_doc)

        result = {
            "count": count,
            "max_score": max_score,
            "min_score": min_score,
            "docs": matched_doc,
        }

        return result

    def __str__(self) -> str:
        return "{}:{}/{}".format(
            self._config["host"],
            self._config["port"],
            self._config["index"],
        )

    def __repr__(self) -> str:
        return "{}(host={!r},port={},index={!r},list_fields={!r},K={})".format(
            self.__class__.__name__,
            self._config["host"],
            self._config["port"],
            self._config["index"],
            self._list_fields,
            self.K,
        )
