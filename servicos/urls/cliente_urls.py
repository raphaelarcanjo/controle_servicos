from django.urls import path
from servicos import views


urlpatterns = [
    path('novocliente', views.adicionarCliente, name='novocliente'),
    path('editarcliente/<int:cliente_id>', views.editarCliente, name='editarcliente'),
    path('removercliente/<int:cliente_id>', views.removerCliente, name='removercliente'),
]
