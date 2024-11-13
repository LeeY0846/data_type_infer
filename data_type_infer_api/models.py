from django.db import models

# Superuser
# username: AdMiN
# password: aDminAdMIn

# Create your models here.
class DataFile(models.Model):
  filename = models.CharField(max_length=180, name="filename")
  file = models.FileField(upload_to="uploads/", name="file")
  
  def __str__(self):
    return self.filename
  
class ColumnDataType(models.Model):
  column_id = models.IntegerField()
  column_type = models.CharField(max_length=40)
  file = models.ForeignKey(DataFile, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.file}-{self.column_id}-{self.column_type}"