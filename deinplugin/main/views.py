
import yaml
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Plugin, Dependency, Introduction, Description, PluginName, Download
from .serializers import PluginSerializer
from .utils import get_plugin_info


# # Create your views here.
# def login(request):
#     return render(request, 'login.html')


# @login_required
# def home(request):
#     # user = User.objects.get(username=request.user)
#     # social = user.social_auth.get(provider='github')
#     # access_token = social.extra_data['access_token']

#     return render(request, 'home.html', {'res': content})
class PluginViewSet(viewsets.ModelViewSet):
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer

    def get_queryset(self):
        return Plugin.objects.filter(state='approved')

    def create(self, request, **kwargs):
        github_url = request.data.get('github_url')
        content = get_plugin_info(github_url)

        if content is None:
            return Response({'error': 'Could not find deinplugin.yaml'}, status=status.HTTP_400_BAD_REQUEST)

        deinplugin_yaml = yaml.load(content, Loader=yaml.FullLoader)

        try:
            plugin = Plugin.objects.create(
                specVersion=deinplugin_yaml.get('specVersion'),
                type=deinplugin_yaml.get('type'),
                mail= request.data.get('mail', None),
                supportedPlatforms=deinplugin_yaml.get('supportedPlatforms'),
                supportedGameVersions=deinplugin_yaml.get('supportedGameVersions'),
                category=deinplugin_yaml.get('category'),
                authors=deinplugin_yaml.get('authors'),
                tags=deinplugin_yaml.get('tags'),
                images=deinplugin_yaml.get('images'),
                icon=deinplugin_yaml.get('icon'),
                videoSources=deinplugin_yaml.get('videoSources'),
                github_url=github_url)
            plugin.save()
        # Exception when unique constraint is violated
        except IntegrityError as e:
            return Response({'message': 'Plugin could not be created, probably already exists', 'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({'message': 'deinplugin.yaml is not valid', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
                depend = Dependency.objects.create(plugin=plugin, url=dependency['url'], versionRange=dependency['versionRange'], required=dependency['required'])
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

        return Response({'success': 'Plugin created'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='wipe')
    def wipe(self, request, pk=None):
        Plugin.objects.all().delete()
        return Response({'success': 'Plugins wiped'}, status=status.HTTP_200_OK)
