from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("search/", include("apps.search.urls")),
]
