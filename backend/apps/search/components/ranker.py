from typing import Dict, List, Union

import grpc

from .encoder_pb2 import RerankDocumentsRequest
from .encoder_pb2_grpc import EncoderStub


class Reranker:
    """Control connection to FAISS index server
    to conduct retrieval and re-ranking.
    """
    def __init__(self, host: str, port: int, L: int=10) -> None:
        self._config = {
            "host": host,
            "port": port,
        }
        self.L = L
        self.conn = self.get_encoder_connection(host, port)

    def get_encoder_connection(self, host: str, port: int):
        """Establish connection to the gRPC server."""
        server_address = f"{host}:{port}"
        channel = grpc.insecure_channel(server_address)
        stub = EncoderStub(channel)
        return stub

    # Step 6, 7, 8, 9, 10
    def rerank(
        self,
        list_sent_ids: List[int],
        query: str,
    ) -> List[Dict[str, Union[int, float]]]:
        """Return list of IDs of relevant sentences after re-ranking.

            Args:
                list_sent_ids (List[int]): list of ids of corresponding sentences of K docs
                query (str): user's query

            Returns:
                list: consisting of ids and distances (scores) of ranked sentences
                and their distant (or score) according to relevant docs.
                    Format:
                    [
                        {
                            "id": <int>,
                            "distance": <float>
                        },
                        ...
                    ]
        """
        response = self.conn.RetrieveRerankDocuments(
            RerankDocumentsRequest(
                ids=list_sent_ids,
                query=query,
                k=self.L,
            ),
        )

        # Return list of sentences' id and their distance (cosine score)
        # compared with the given question query
        relevant_sentences = [
            {
                "id": match.id,
                "distance": match.distance,
            }
            for match in response.matches
        ]

        return relevant_sentences

    def __str__(self) -> str:
        return "{!r}:{}".format(
            self._config["host"],
            self._config["port"],
        )

    def __repr__(self) -> str:
        return "{}(host={!r},port={},L={})".format(
            self.__class__.__name__,
            self._config["host"],
            self._config["port"],
            self.L,
        )
