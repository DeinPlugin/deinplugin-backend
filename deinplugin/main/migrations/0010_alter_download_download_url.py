# Generated by Django 4.1.2 on 2022-12-18 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_rename_url_download_download_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='download_url',
            field=models.CharField(max_length=500),
        ),
    ]
