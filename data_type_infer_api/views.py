from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from data_type_infer_api.models import DataFile, ColumnDataType
from .models import DataFile
from .forms import DataFileForm
import json

# Create your views here.

class DatasetFileApiView(APIView):
  def get(self, request, *args, **kwargs):
    """
    Get the dataset file with the given id
    """
    data = DataFile.objects.all().values("filename", "pk")
    return Response(data, status = status.HTTP_200_OK, content_type="application/json")
  
  def post(self, request, *args, **kwargs):
    form = DataFileForm(request.POST, request.FILES)
    if (form.is_valid):
      form.save()
      return Response(status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, *args, **kwargs):
    fileID = request.POST.get("id")
    # print(json.load(request.body).id)
    instance = DataFile.objects.get(pk=fileID)
    if not instance:
      return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    instance.delete()
    return Response({}, status=status.HTTP_200_OK)
  