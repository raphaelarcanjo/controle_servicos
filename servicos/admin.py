from django.contrib import admin
from servicos import models


admin.site.register(models.Cliente)
admin.site.register(models.Servico)
admin.site.register(models.Mensageiro)
admin.site.register(models.StatusServico)
