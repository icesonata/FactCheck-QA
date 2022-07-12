from concurrent import futures
import grpc
import logging

import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

import encoder_pb2
import encoder_pb2_grpc

ROOT_DIR = "/home/azureuser/FactCheck-QA/"    # Change this
DATA_DIR = "dataset/MLQA/Test/"

EMBEDDING_MODEL = "distiluse-base-multilingual-cased-v2"
# https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v2
FEATURE_SIZE = 512
FAISS_INDEX = os.path.join(
    ROOT_DIR,
    DATA_DIR,
    "sentence.index"
)

encoder = SentenceTransformer(EMBEDDING_MODEL)


class EncoderServicer(encoder_pb2_grpc.EncoderServicer):

    def __init__(self):
        self.index = faiss.read_index(
            os.path.join(FAISS_INDEX)
        )

    def FindTopKDocuments(self, request, context):
        matches = []    # List of DocumentMatch
        error = None    # Enumerate Error of SearchResponse

        try:
            query = request.query
            query_vector = encoder.encode([preprocessed_query])
            k = request.k

            D_title, I_title = self.index_title.search(query_vector, k)
            D_content, I_content = self.index_content.search(query_vector, k)

            # # Weighting title over content
            # boost = 0.3    # Edit this number
            # for i in range(len(D_title)):
            #     D_title[i] += boost
            #     # D_content[i] += boost

            # Group Index number and Distance score for group of results from each index
            res_title = list(zip(I_title.tolist()[0], D_title.tolist()[0]))
            res_content = list(
                zip(I_content.tolist()[0], D_content.tolist()[0]))
            # print('From title', res_title)
            # print('From content', res_content)

            # Combine the results while getting rid of duplication
            comb = list(set(res_title + res_content))
            # Sort by distance scores
            comb = sorted(comb, key=lambda tup: tup[1], reverse=True)
            # Sort by distance scores by ascending,
            # the smaller the distance, the better result for user's query
            # comb = sorted(comb, key=lambda tup: tup[1])

            # print(comb[:5])
            # Get top 5
            for idx, d in comb[:k]:
                matches.append(encoder_pb2.DocumentMatch(id=idx, distance=d))

            if len(matches) > 0:
                error = encoder_pb2.SearchResponse.Error.NO_ERROR
            else:
                error = encoder_pb2.SearchResponse.Error.INDEX_IS_NOT_READY

        except Exception as e:
            print(e)
            error = encoder_pb2.SearchResponse.Error.UNKNOWN_ERROR

        return encoder_pb2.SearchResponse(
            matches=matches,
            error=error
        )

    def RetrieveRerankDocuments(self, request, context):
        """Retrieve and re-rank top K from the given documents."""
        matches = []
        error = None
        try:
            # Preprocess and encode user querystring
            query = request.query
            query_vector = encoder.encode([query])

            # Get K parameter and list of sentences' IDs
            k = request.k
            list_candidate_ids = request.ids

            # Initialize an archive for converting list of tuple into list of IDs
            embeddings = np.array([
                self.index.reconstruct(id_) for id_ in list_candidate_ids
            ])

            new_index = faiss.IndexIDMap(faiss.IndexFlatIP(FEATURE_SIZE))
            new_index.add_with_ids(
                embeddings,
                np.array(list_candidate_ids),
            )

            distances, indices = new_index.search(query_vector, k)

            # Normalization
            distances = normalize(distances)

            result = list(zip(indices.tolist()[0], distances.tolist()[0]))

            # For debugging
            logging.debug(f"Result (Distance, Index):\n{result}")

            # Take only distinct documents (no duplicate)
            cnt = 0
            track_ids = set()
            for idx, d in result:
                # matches.append(encoder_pb2.DocumentMatch(id=idx, distance=d))
                if cnt == k:
                    break
                elif idx not in track_ids:
                    matches.append(
                        encoder_pb2.DocumentMatch(id=idx, distance=d))
                    track_ids.add(idx)
                    cnt += 1

            if len(matches) > 0:
                error = encoder_pb2.SearchResponse.Error.NO_ERROR
            else:
                error = encoder_pb2.SearchResponse.Error.INDEX_IS_NOT_READY
        except Exception as err:
            error = encoder_pb2.SearchResponse.Error.UNKNOWN_ERROR

        return encoder_pb2.SearchResponse(
            matches=matches,
            error=error
        )

    def Sync(self, request, context):
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    encoder_pb2_grpc.add_EncoderServicer_to_server(
        EncoderServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    serve()
