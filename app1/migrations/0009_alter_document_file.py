# Generated by Django 5.0.6 on 2024-06-06 15:24

import app1.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_document_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=app1.models.user_directory_path),
        ),
    ]
