# Generated by Django 5.0.6 on 2024-05-31 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_delete_userkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='encryption_key',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='iv',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]