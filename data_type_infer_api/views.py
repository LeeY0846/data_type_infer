from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from data_type_infer_api.models import DataFile, ColumnDataType
from .models import DataFile, ColumnDataType
from .forms import DataFileForm
from .utils import get_inferred_types, get_chunked_typed_data, CHUNK_SIZE
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
    if form.is_valid:
      form.save()
      return Response(status=status.HTTP_201_CREATED)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, *args, **kwargs):
    fileID = request.POST.get("id")
    # print(json.load(request.body).id)
    instance = DataFile.objects.get(pk=fileID)
    if not instance:
      return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    instance.delete()
    return Response({}, status=status.HTTP_200_OK)
  
class DatasetApiView(APIView):
  def get(self, request, file_id, chunk_id, *args, **kwargs):
    instance = DataFile.objects.get(pk=file_id)
    if not instance:
      return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    columnTypes = ColumnDataType.objects.filter(file_id=file_id)
    types = {}
    if len(columnTypes) == 0:
      types = get_inferred_types(instance.file.path)
      for col in types:
        ColumnDataType.objects.create(column_name=col, column_type=types[col], file=instance)
    else:
      for type in columnTypes:
        types[type.column_name] = type.column_type
    data = get_chunked_typed_data(instance.file.path, CHUNK_SIZE * chunk_id, types)
    return Response({"name":instance.filename, "types": json.dumps(types), "data": data["data"], "ended": data["ended"], "chunk": chunk_id}, status=status.HTTP_200_OK)