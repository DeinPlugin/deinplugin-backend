# Generated by Django 4.1.2 on 2022-12-24 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_plugin_supportedplatforms'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependency',
            name='name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
    ]
