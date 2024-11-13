from django.db import models

# Create your models here.
class DataFile(models.Model):
  filename = models.CharField(max_length=180)
  update_date = models.DateTimeField("date updated")
  
class ColumnDataType(models.Model):
  column_id = models.IntegerField()
  column_type = models.CharField(max_length=40)
  file = models.ForeignKey(DataFile, on_delete=models.CASCADE)