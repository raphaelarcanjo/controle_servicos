from django.urls import path
from servicos.views import ConfigView as views


app_name = 'config'
urlpatterns = [
    path('adicionarmensageiro', views.adicionarMensageiro, name='adicionarmensageiro'),
    path('removermensageiro/<int:mensageiro_id>', views.removerMensageiro, name='removermensageiro'),
    path('adicionarstatus', views.adicionarStatus, name='adicionarstatus'),
    path('removerstatus/<int:status_id>', views.removerStatus, name='removerstatus')
]
