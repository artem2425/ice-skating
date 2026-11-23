from django.urls import path
from . import views
urlpatterns = [path('', views.rink_list, name='rink_list')]
