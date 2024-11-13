# Generated by Django 5.1.3 on 2024-11-13 04:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=180)),
                ('update_date', models.DateTimeField(verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='ColumnDataType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_id', models.IntegerField()),
                ('column_type', models.CharField(max_length=40)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_type_infer_api.datafile')),
            ],
        ),
    ]