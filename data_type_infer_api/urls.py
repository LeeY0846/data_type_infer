from django.urls import path
from .views import DatasetFileApiView

urlpatterns = [
    path("dataset", DatasetFileApiView.as_view()),
]