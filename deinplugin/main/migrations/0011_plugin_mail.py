# Generated by Django 4.1.2 on 2022-12-20 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_download_download_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='plugin',
            name='mail',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]