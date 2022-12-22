import logging
import yaml
import time
from random import uniform
from django.db import transaction

from .models import Plugin, Dependency, Introduction, Description, PluginName, Download
from .utils import get_plugin_info, stable_string_hash

logger = logging.getLogger('pluginmeta')
logger.setLevel(logging.DEBUG)
logging_handler = logging.FileHandler('/var/www/logs/pluginmeta.log')
logging_handler.setLevel(logging.DEBUG)
Logging_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging_handler.setFormatter(Logging_formatter)
logger.addHandler(logging_handler)


def do_plugin_update_cycle():
    logger.info("Starting plugin update cycle.")
    try:
        for plugin in Plugin.objects.all():
            try_update_plugin_if_changed(plugin)
            time.sleep(uniform(3, 10) * 60)
        logger.info("Plugin update cycle completed.")
    except Exception as e:
        logger.exception("Error in plugin update cycle", exc_info=e)


def try_update_plugin_if_changed(plugin: Plugin):
    content = get_plugin_info(plugin.github_url)
    if content is None:
        logger.error("Failed to retrieve plugin metadata file from %s", plugin.github_url)
        return False

    content_hash = stable_string_hash(content)
    if content_hash == plugin.last_yaml_hash:
        logger.debug("Plugin metadata file has not changed: %s", plugin.github_url)
        return False

    try:
        with transaction.atomic():
            clear_plugin_meta(plugin)
            fill_plugin_meta_from_yaml(plugin, content)
        logger.info("Successfully updated plugin metadata for: %s", plugin.github_url)
        return True
    except Exception as e:
        logger.exception("Failed to update plugin metadata for %s", plugin.github_url, exc_info=e)
        return False


def clear_plugin_meta(plugin: Plugin):
    PluginName.objects.filter(plugin=plugin).delete()
    Dependency.objects.filter(plugin=plugin).delete()
    Introduction.objects.filter(plugin=plugin).delete()
    Description.objects.filter(plugin=plugin).delete()
    Download.objects.filter(plugin=plugin).delete()


def fill_plugin_meta_from_yaml(plugin: Plugin, yaml_str: str):
    deinplugin_yaml = yaml.load(yaml_str, Loader=yaml.FullLoader)
    plugin.specVersion = deinplugin_yaml.get('specVersion')
    plugin.type = deinplugin_yaml.get('type')
    plugin.supportedPlatforms = deinplugin_yaml.get('supportedPlatforms')
    plugin.supportedGameVersions = deinplugin_yaml.get('supportedGameVersions')
    plugin.category = deinplugin_yaml.get('category')
    plugin.authors = deinplugin_yaml.get('authors')
    plugin.tags = deinplugin_yaml.get('tags')
    plugin.images = deinplugin_yaml.get('images')
    plugin.icon = deinplugin_yaml.get('icon')
    plugin.videoSources = deinplugin_yaml.get('videoSources')
    plugin.last_yaml_hash = stable_string_hash(yaml_str)
    plugin.save()

    names = deinplugin_yaml['name']
    if isinstance(names, dict):
        for key, value in names.items():
            name = PluginName.objects.create(plugin=plugin, key=key, value=value)
            name.save()
    else:
        name = PluginName.objects.create(plugin=plugin, key=None, value=names)
        name.save()

    if 'dependencies' in deinplugin_yaml:
        dependencies = deinplugin_yaml['dependencies']
        for dependency in dependencies:
            depend = Dependency.objects.create(
                plugin=plugin, url=dependency['url'],
                versionRange=dependency['versionRange'],
                required=dependency['required'])
            depend.save()

    introductions = deinplugin_yaml['introduction']
    if isinstance(introductions, dict):
        for key, value in introductions.items():
            intro = Introduction.objects.create(plugin=plugin, key=key, value=value)
            intro.save()
    else:
        intro = Introduction.objects.create(plugin=plugin, key=None, value=introductions)
        intro.save()

    descriptions = deinplugin_yaml['description']
    if isinstance(descriptions, dict):
        for key, value in descriptions.items():
            desc = Description.objects.create(plugin=plugin, key=key, value=value)
            desc.save()
    else:
        desc = Description.objects.create(plugin=plugin, key=None, value=descriptions)
        desc.save()

    download = deinplugin_yaml.get('download')
    if download is not None:
        download = Download.objects.create(plugin=plugin, download_url=download['url'], name=download['name'])
        download.save()
