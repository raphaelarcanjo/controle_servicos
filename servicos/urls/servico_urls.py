from django.urls import path
from servicos.views import ServicoView as views


app_name = 'servico'
urlpatterns = [
    path('novoservico', views.adicionarServico, name='novoservico'),
    path('editarservico/<int:servico_id>', views.editarServico, name='editarservico'),
    path('removerservico/<int:servico_id>', views.removerServico, name='removerservico')
]
