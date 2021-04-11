from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('novocliente', views.adicionarCliente, name='novocliente'),
    path('novoservico', views.adicionarServico, name='novoservico'),
    path('editarservico/<int:servico_id>', views.editarServico, name='editarservico'),
    path('removerservico/<int:servico_id>', views.removerServico, name='removerservico'),
    path('editarcliente/<int:cliente_id>', views.editarCliente, name='editarcliente'),
    path('removercliente/<int:cliente_id>', views.removerCliente, name='removercliente'),
]
