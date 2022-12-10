from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.
class Plugin(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    specVersion = models.IntegerField(default=1)


    class PluginType(models.TextChoices):
        plugin = 'plugin', 'Plugin'
        lib = 'lib', 'Lib'
    type = models.CharField(choices=PluginType.choices, default=PluginType.plugin, max_length=100)

    class Platforms(models.TextChoices):
        spigot = 'spigot', 'Spigot'
        paper = 'paper', 'Paper'
        sponge = 'sponge', 'Sponge'

    supportedPlatforms = ArrayField(models.CharField(choices=Platforms.choices, max_length=100), null=True, blank=True)

    class Categories(models.TextChoices):
        ADMINTOOL = 'admintool', 'AdminTool'
        DEVTOOL = 'devtool', 'DevTool'
        CHAT = 'chat', 'Chat'
        ECONOMY = 'economy', 'Economy'
        GAME = 'game', 'Game'
        PROTECTION = 'protection', 'Protection'
        ROLEPLAY = 'roleplay', 'Roleplay'
        WORLDMANAGEMENT = 'worldmanagement', 'WorldManagement'
        MISC = 'misc', 'Misc'
    
    supportedGameVersions = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    authors = ArrayField(models.CharField(max_length=100))
    tags = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    images = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    icon = models.CharField(max_length=100)
    videoSources = ArrayField(models.CharField(max_length=100), null=True, blank=True)

    github_url = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Dependency(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    versionRange = models.CharField(max_length=100)
    required = models.BooleanField(default=True)

class Introduction(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    key = models.CharField(max_length=5)
    value = models.TextField()

class Description(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    key = models.CharField(max_length=5)
    value = models.TextField()

class Installation(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    key = models.CharField(max_length=5)
    value = models.TextField()