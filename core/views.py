import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from property.models import Category, Property

from .forms import SignupForm
from configparser import ConfigParser


cfg = ConfigParser()
cfg.read("../conf/cfg.conf")
API_KEY = cfg.get('APP_CONF', 'moralis_api_key')

if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit


def index(request):
    properties = Property.objects.filter(for_sale=True)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'properties': properties,
    })


def contact(request):
    return render(request, 'core/contact.html')

def profile(request):
    return render(request, 'core/profile.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })


def moralis_auth(request):
    return render(request, 'core/sync.html', {})


def my_profile(request):
    return render(request, 'core/profile.html', {})


def request_message(request):
    data = json.loads(request.body)
    print(data)
    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "localhost",
      "chainId": 1337,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": cfg.get('APP_CONF', 'ganache_url'),
      "expirationTime": "2025-01-01T00:00:00.000Z",
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})
    return JsonResponse(json.loads(x.text))
def verify_message(request):
    data = json.loads(request.body)
    print(data)
    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))