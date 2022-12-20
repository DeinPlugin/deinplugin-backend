from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class Plugin(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    
    mail = models.EmailField(max_length=254, null=True, blank=True)
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
    icon = models.CharField(max_length=100, null=True, blank=True)
    videoSources = ArrayField(models.CharField(max_length=100), null=True, blank=True)

    github_url = models.CharField(max_length=100, unique=True)

    class State(models.TextChoices):
        pending = 'pending', 'Pending'
        approved = 'approved', 'Approved'
        rejected = 'rejected', 'Rejected'

    state = models.CharField(choices=State.choices, default=State.pending, max_length=100)


class PluginName(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='names')
    key = models.CharField(max_length=5, null=True, blank=True)
    value = models.CharField(max_length=100)


class Dependency(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='dependencies')
    url = models.CharField(max_length=100)
    versionRange = models.CharField(max_length=100)
    required = models.BooleanField(default=True)


class Introduction(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='introductions')
    key = models.CharField(max_length=5, null=True, blank=True)
    value = models.TextField()


class Description(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='descriptions')
    key = models.CharField(max_length=5, null=True, blank=True)
    value = models.TextField()


class Installation(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='installations')
    key = models.CharField(max_length=5, null=True, blank=True)
    value = models.TextField()


class Download(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='download')
    name = models.CharField(max_length=30, null=True, blank=True)
    download_url = models.CharField(max_length=500)
