from typing import Dict, List, Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBIndex:
    """Control over database index to conduct specific tasks."""

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        pwd: str,
        db_name: str,
        db_sent_table: str,
    ) -> None:
        self._config = {
            "host": host,
            "port": port,
            "user": user,
            "name": db_name,
        }
        # create engine connecting to the database
        self.engine = create_engine(
            f"mysql+pymysql://{user}:{pwd}@"
            f"{host}:{port}/{db_name}",
            pool_size=50,
            max_overflow=10,
        )
        # self.conn = scoped_session(sessionmaker(bind=self.engine))
        self.Session = sessionmaker(bind=self.engine)
        self.db_sent_table = db_sent_table

    # Step 11, 12
    def retrieve_sentences(self, list_ids: List[int]) -> Dict[int, str]:
        """Return list of L sentences in text from the database.

            Args:
                list_ids (List[int]): list of sentences' index

            Returns:
                dict: mappings between sentence's index number and sentence's value
                    Format:
                    {
                        <int>: <str>,
                        ...
                    }
        """
        # docs = self.conn.execute(
        #     f"select id, sentence from {self.db_sent_table} "
        #     f"where id in ({','.join([str(id_) for id_ in list_ids])})"
        # )
        with self.Session() as session:
            docs = session.execute(
                f"select id, sentence from {self.db_sent_table} "
                f"where id in ({','.join([str(id_) for id_ in list_ids])})"
            )

        result = {entry[0]: entry[1] for entry in docs}  # 0->id; 1->sentence
        return result

    def get_doc_id(self, sent_id: int) -> int:
        """Return ID of relevant document based on given sentence's ID.

            Args:
            - sent_id: sentence's index number

            Returns:
            - int: index of the document corresponding the the given sentence
        """
        # query = self.conn.execute(
        #     f"select doc_id from {self.db_sent_table} "
        #     f"where id={sent_id}"
        # ).fetchone()
        with self.Session() as session:
            query = session.execute(
                f"select doc_id from {self.db_sent_table} "
                f"where id={sent_id}"
            ).fetchone()

        result = dict(query)
        doc_id = result.get("doc_id")

        return doc_id

    # Step 4, 5

    def get_sentences_ids(
        self,
        doc_ids: List[int],
    ) -> List[Tuple[int, int]]:
        """Retrieve list of IDs of sentences for corresponding documents.

            Args:
                doc_ids (List[int]): list of sentences' index

            Returns:
                list: list of tuples (start/end indexes) for sentences of each doc  
        """
        # query_result = self.conn.execute(
        #     f"select id from {self.db_sent_table} "
        #     f"where doc_id in ({','.join([str(id_) for id_ in doc_ids])})"
        # ).fetchall()
        with self.Session() as session:
            query_result = session.execute(
                f"select id from {self.db_sent_table} "
                f"where doc_id in ({','.join([str(id_) for id_ in doc_ids])})"
            ).fetchall()
        sentences_ids = [elem[0] for elem in query_result]

        return sentences_ids

    def __str__(self) -> str:
        return "mysql+pymysql://{}:<>@{}:{}/{}".format(
            self._config["user"],
            self._config["host"],
            self._config["port"],
            self._config["name"],
        )

    def __repr__(self) -> str:
        return "{}(host={!r},port={},user={!r},pwd=<>,db_name={!r},db_sent_table={!r})".format(
            self.__class__.__name__,
            self._config["host"],
            self._config["port"],
            self._config["user"],
            self._config["name"],
            self.db_sent_table,
        )
