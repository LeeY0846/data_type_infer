# Generated by Django 5.1.3 on 2024-11-13 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_type_infer_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafile',
            name='update_date',
        ),
        migrations.AddField(
            model_name='datafile',
            name='file',
            field=models.FileField(default=1, upload_to='uploads/'),
            preserve_default=False,
        ),
    ]
