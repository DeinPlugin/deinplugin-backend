from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Plugin
from .pluginmeta import fill_plugin_meta_from_yaml
from .serializers import PluginSerializer
from .utils import get_plugin_info
from django.conf import settings


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

    # override get method
    def list(self, request, **kwargs):
        secret = request.query_params.get('secret', None)
        if secret is None:
            serializer = PluginSerializer(Plugin.objects.filter(state='approved'), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # get REQUEST_SECRET from settings.py
        if secret == settings.REQUEST_SECRET:
            serializer = PluginSerializer(Plugin.objects.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # return unauthorized if secret is invalid
            return Response({'error': 'Invalid secret'}, status=status.HTTP_401_UNAUTHORIZED)


    def update(self, request, **kwargs):
        secret = request.data.get('secret', None)
        if secret == settings.REQUEST_SECRET:
            return super().update(request, **kwargs)
        else:
            return Response({'error': 'Invalid secret'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, **kwargs):
        github_url = request.data.get('github_url')
        mail = request.data.get('mail', None)
        content = get_plugin_info(github_url)
        
        if content is None:
            return Response({'error': 'Could not find deinplugin.yaml'}, status=status.HTTP_400_BAD_REQUEST)
        
        existing_plugins = Plugin.objects.filter(github_url=github_url)
        if existing_plugins.exists():
            if existing_plugins.first().state == 'rejected':
                # resubmission of a rejected plugin
                try:
                    with transaction.atomic():
                        plugin = existing_plugins.first()
                        fill_plugin_meta_from_yaml(plugin, content)
                        plugin.state = 'pending'
                        plugin.save()
                except Exception as e:
                    return Response({'message': 'Failed to create plugin, probably because deinplugin.yaml is not valid', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)    
                # plugin successfully submitted again
                return Response({'success': 'Plugin submitted'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Plugin already submitted'}, status=status.HTTP_409_CONFLICT)

        try:
            with transaction.atomic():
                plugin = Plugin(mail=mail, github_url=github_url)
                fill_plugin_meta_from_yaml(plugin, content)
        except Exception as e:
            return Response({'message': 'Failed to create plugin, probably because deinplugin.yaml is not valid', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Plugin created'}, status=status.HTTP_201_CREATED)

