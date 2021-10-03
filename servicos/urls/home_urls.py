from django.urls import path
from servicos.views import HomeView as views


app_name = 'home'
urlpatterns = [
    path('', views.index, name='home'),
    path('relatorio', views.relatorio, name='relatorio'),
    path('config', views.config, name='config')
]
