from rest_framework import serializers
from .models import Plugin, Dependency, Introduction, Description


class PluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin
        fields = (
            'uuid',
            'name',
            'specVersion',
            'type',
            'supportedPlatforms',
            'supportedGameVersions',
            'category',
            'authors',
            'tags',
            'images',
            'icon',
            'videoSources',
            'version',
            'github_url',
        )

class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = (
            'plugin',
            'url',
            'versionRange',
            'required',
        )

class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        fields = (
            'key',
            'value',
        )

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = (
            'key',
            'value',
        )
