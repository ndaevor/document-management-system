# Generated by Django 5.0.6 on 2024-06-04 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_document_file_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='salt',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]