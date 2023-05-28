from django.urls import path

from . import views

app_name = 'property'

urlpatterns = [
    path('', views.get_properties, name='get_properties'),
    path('new/', views.create_new_property, name='create_new_property'),
    path('<int:pk>/', views.get_property_details, name='get_property_details'),
    path('<int:pk>/delete/', views.delete_property, name='delete_property'),
    path('<int:pk>/edit/', views.edit_property, name='edit_property'),
]
