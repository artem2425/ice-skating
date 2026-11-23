from django.urls import include, path
from django.views.defaults import page_not_found
urlpatterns = [path('', include('homepage.urls')), path('rinks/', include('rinks.urls')), path('skating/', include('skating.urls'))]
