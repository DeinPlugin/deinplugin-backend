from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Plugin
from .pluginmeta import fill_plugin_meta_from_yaml
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
        mail = request.data.get('mail', None)
        content = get_plugin_info(github_url)
        
        if content is None:
            return Response({'error': 'Could not find deinplugin.yaml'}, status=status.HTTP_400_BAD_REQUEST)

        if Plugin.objects.filter(github_url=github_url).exists():
            return Response({'message': 'Plugin already submitted'}, status=status.HTTP_409_CONFLICT)

        try:
            with transaction.atomic():
                plugin = Plugin(mail=mail, github_url=github_url)
                fill_plugin_meta_from_yaml(plugin, content)
        except Exception as e:
            return Response({'message': 'Failed to create plugin, probably because deinplugin.yaml is not valid', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Plugin created'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='wipe')
    def wipe(self, request, pk=None):
        Plugin.objects.all().delete()
        return Response({'success': 'Plugins wiped'}, status=status.HTTP_200_OK)
