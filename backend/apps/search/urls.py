from django.urls.conf import path

from . import views

urlpatterns = [
    path(
        "relevance/",
        views.SearchRelevanceView.as_view(),
        name="search-relevance",
    ),
    path(
        "inference/",
        views.InferenceView.as_view(),
        name="inference",
    ),
    path(
        "answering/",
        views.AnsweringView.as_view(),
        name="question-answering",
    ),
]