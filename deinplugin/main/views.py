from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# import user
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    user = User.objects.get(username=request.user)
    print(user)
    social = user.social_auth.get(provider='github')
    access_token = social.extra_data['access_token']
    print(social.extra_data)
    print(access_token)
    return render(request, 'home.html', {'token': access_token})