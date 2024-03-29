# Generated by Django 4.1.2 on 2022-12-24 12:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_plugin_created_at_plugin_last_yaml_hash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plugin',
            name='supportedPlatforms',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('spigot', 'Spigot'), ('paper', 'Paper'), ('sponge', 'Sponge'), ('minestom', 'Minestom')], max_length=100), blank=True, null=True, size=None),
        ),
    ]
