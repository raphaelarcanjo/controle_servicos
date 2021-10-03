from django.urls import path
from servicos import views


urlpatterns = [
    path('novoservico', views.adicionarServico, name='novoservico'),
    path('editarservico/<int:servico_id>', views.editarServico, name='editarservico'),
    path('removerservico/<int:servico_id>', views.removerServico, name='removerservico')
]
