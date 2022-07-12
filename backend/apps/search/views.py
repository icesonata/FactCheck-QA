import json

from django.http import HttpResponse, JsonResponse
from rest_framework import status, views

from .components.config import RETRIEVER_SETTING
from .components.retriever import Retriever

retriever_client = Retriever(**RETRIEVER_SETTING)


class SearchRelevanceView(views.APIView):
    """An API view for searching for relevant document."""

    def post(self, request, *args, **kwargs):
        query = request.POST.get("data", "")
        result = {}
        if query:
            result = retriever_client.retrieve(query)

        # Ref: https://stackoverflow.com/a/34805851
        return HttpResponse(
            json.dumps(result, ensure_ascii=False),
            content_type="application/json",
        )


class InferenceView(views.APIView):
    """An API view for confidence examination for a given information."""

    def post(self, request, *args, **kwargs):
        # query = "Đến năm 9000 BP, Châu Âu đã có rừng bao phủ toàn bộ"
        query = request.POST.get("data", "")
        result = {}
        if query:
            result = retriever_client.retrieve_inference(query)

        # Ref: https://stackoverflow.com/a/34805851
        return HttpResponse(
            json.dumps(result, ensure_ascii=False),
            content_type="application/json",
        )


class AnsweringView(views.APIView):
    """An API view for answering a given question."""

    def post(self, request, *args, **kwargs):
        # query = "Bao nhiêu ngày mùa đông dưới 0 độ?"
        query = request.POST.get("data", "")
        result = {}
        if query:
            result = retriever_client.retrieve_answer(query)

        # Ref: https://stackoverflow.com/a/34805851
        return HttpResponse(
            json.dumps(result, ensure_ascii=False),
            content_type="application/json",
        )
