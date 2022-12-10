from rest_framework import serializers
from .models import Plugin, PluginName, Dependency, Introduction, Description, Installation

class PluginNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginName
        fields = (
            'key',
            'value',
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

class InstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = (
            'key',
            'value',
        )


class PluginSerializer(serializers.ModelSerializer):
    names = PluginNameSerializer(many=True)
    dependencies = DependencySerializer(many=True)
    introductions = IntroductionSerializer(many=True)
    descriptions = DescriptionSerializer(many=True)
    installations = InstallationSerializer(many=True)
    class Meta:
        model = Plugin
       
        fields = (
            'uuid',
            'names',
            'descriptions',
            'specVersion',
            'introductions',
            'type',
            'supportedPlatforms',
            'dependencies',
            'supportedGameVersions',
            'installations',
            'category',
            'authors',
            'tags',
            'images',
            'icon',
            'videoSources',
            'github_url',
        )
