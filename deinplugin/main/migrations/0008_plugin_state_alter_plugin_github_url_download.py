# Generated by Django 4.1.2 on 2022-12-18 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_plugin_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='plugin',
            name='state',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='github_url',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('url', models.CharField(max_length=100)),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='download', to='main.plugin')),
            ],
        ),
    ]