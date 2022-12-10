
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.models import User

from .utils import get_plugin_info
from .models import Plugin, Dependency, Introduction, Description
from .serializers import PluginSerializer

import yaml

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


    def create(self, request):
        github_url = request.data.get('github_url')
        content = get_plugin_info(github_url)
        
        if content == None:
            return Response({'error': 'Could not find deinplugin.yaml'}, status=status.HTTP_400_BAD_REQUEST)
        deinplugin_yaml = yaml.load(content, Loader=yaml.FullLoader)
        try:
            plugin = Plugin.objects.create(
                name=deinplugin_yaml['name'],
                specVersion=deinplugin_yaml['specVersion'], 
                type=deinplugin_yaml['type'], 
                supportedPlatforms=deinplugin_yaml['supportedPlatforms'], 
                supportedGameVersions=deinplugin_yaml['supportedGameVersions'], 
                category=deinplugin_yaml['category'], 
                authors=deinplugin_yaml['authors'], 
                tags=deinplugin_yaml['tags'], 
                images=deinplugin_yaml['images'], 
                icon=deinplugin_yaml['icon'], 
                videoSources=deinplugin_yaml['videoSources'], 
                github_url=github_url)
            plugin.save()
        except KeyError  as e:
            print(e)
            return Response({'error': 'deinplugin.yaml is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        if 'dependencies' in deinplugin_yaml:
            dependencies = deinplugin_yaml['dependencies']
            for dependency in dependencies:
                depend = Dependency.objects.create(plugin=plugin, url=dependency['url'], versionRange=dependency['versionRange'], required=dependency['required'])
                depend.save()
        introductions = deinplugin_yaml['introduction']
        if isinstance(introductions, dict):
            for key,value in introductions.items():
                intro = Introduction.objects.create(plugin=plugin, key=key, value=value)
                intro.save()
        else:
            intro = Introduction.objects.create(plugin=plugin, key=None, value=introductions)
            intro.save()
        descriptions = deinplugin_yaml['description']
        if isinstance(descriptions, dict):
            for key,value in descriptions.items():
                desc = Description.objects.create(plugin=plugin, key=key, value=value)
                desc.save()
        else:
            desc = Description.objects.create(plugin=plugin, key=None, value=descriptions)
            desc.save()
        return Response({'success': 'Plugin created'}, status=status.HTTP_201_CREATED)


