from django.urls import path
from servicos import views


urlpatterns = [
    path('', views.index, name='home'),
    path('relatorio', views.relatorio, name='relatorio'),
    path('config', views.config, name='config')
]
