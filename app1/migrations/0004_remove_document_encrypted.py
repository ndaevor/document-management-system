# Generated by Django 5.0.6 on 2024-05-31 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_document_encrypted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='encrypted',
        ),
    ]
