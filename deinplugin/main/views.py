from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .utils import get_plugin_info

import yaml

# Create your views here.
def login(request):
    return render(request, 'login.html')




@login_required
def home(request):
    user = User.objects.get(username=request.user)
    social = user.social_auth.get(provider='github')
    access_token = social.extra_data['access_token']
    github_url = 'https://github.com/WeLoveOpenSourcePlugins/memory'

    content = get_plugin_info(github_url)
    if content == None:
        return render(request, 'home.html', {'error': 'Could not find deinplugin.yaml'})

    deinplugin_yaml = yaml.load(content, Loader=yaml.FullLoader)

    return render(request, 'home.html', {'res': content})