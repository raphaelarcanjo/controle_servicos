from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('novocliente', views.adicionarCliente, name='novocliente'),
    path('novoservico', views.adicionarServico, name='novoservico'),
    path('editarservico/<int:servico_id>', views.editarServico, name='editarservico'),
]
