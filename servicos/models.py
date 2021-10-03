from django.db import models


class Mensageiro(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class StatusServico(models.Model):
    nome = models.CharField(max_length=12)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=80)
    contato = models.CharField(max_length=(20))
    flag_mensageiro = models.BooleanField(default=0)
    mensageiro = models.ForeignKey(Mensageiro, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    tipo = models.CharField(max_length=80)
    valor = models.FloatField()
    data = models.DateField()
    pago = models.BooleanField(default=0)
    status = models.ForeignKey(StatusServico, on_delete=models.SET_NULL, blank=True, null=True)

    def __int__(self):
        return self.tipo


class ClienteServico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)

    def __int__(self):
        return self.cliente


class Andamento(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusServico, on_delete=models.CASCADE)

    def __int__(self):
        return self.status
