from django.urls import path
from . import views
urlpatterns = [path('', views.skate_list, name='skate_list'), path('statistics/', views.statistics, name='statistics'), path('<slug:slug>/', views.skate_detail, name='skate_detail')]
