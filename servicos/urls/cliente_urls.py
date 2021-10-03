from django.urls import path
from servicos.views import ClienteView as views


app_name = 'cliente'
urlpatterns = [
    path('novocliente', views.adicionarCliente, name='novocliente'),
    path('editarcliente/<int:cliente_id>', views.editarCliente, name='editarcliente'),
    path('removercliente/<int:cliente_id>', views.removerCliente, name='removercliente'),
]
