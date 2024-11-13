from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data_type_infer_api.models import DataFile, ColumnDataType
from django.core import serializers

# Create your views here.

class DatasetApiView(APIView):
  def get(self, request, *args, **kwargs):
    """
    Get the dataset file with the given id
    """
    data = {
      "value": "Hello"
    }
    print(data)
    return Response(data, status = status.HTTP_200_OK, content_type="application/json")
  
  def post(self, request, *args, **kwargs):
    return Response({}, status=status.HTTP_200_OK)