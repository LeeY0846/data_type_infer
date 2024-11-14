from django.urls import path
from .views import DatasetFileApiView, DatasetApiView

urlpatterns = [
    path("dataset", DatasetFileApiView.as_view()),
    path("dataset/<int:file_id>/<int:chunk_id>", DatasetApiView.as_view()),
]