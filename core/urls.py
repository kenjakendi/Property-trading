from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm),kwargs={'redirect_authenticated_user': True}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('moralis_auth/', views.moralis_auth, name='moralis_auth'),
    path('request_message/', views.request_message, name='request_message'),
    path('profile/', views.profile, name='profile'),
    path('verify_message/', views.verify_message, name='verify_message')
]