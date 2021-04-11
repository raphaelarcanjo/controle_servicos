from django.db import models

# Create your models here.


class Cliente(models.Model):
    nome = models.CharField(max_length=80)
    contato = models.CharField(max_length=(20))
    flag_mensageiro = models.BooleanField(blank=True, default=0)
    mensageiro = models.CharField(max_length=(20), null=True, blank=True)

    def __int__(self):
        return self.nome


class Servico(models.Model):
    tipo = models.CharField(max_length=80)
    valor = models.FloatField()
    data = models.DateField()
    pago = models.BooleanField(blank=True, default=0)
    status = models.IntegerField(blank=True, default=1)

    def __int__(self):
        return self.tipo


class ClienteServico(models.Model):
    cliente = models.IntegerField()
    servico = models.IntegerField()

    def __int__(self):
        return self.cliente


class Andamento(models.Model):
    servico = models.IntegerField()
    status = models.IntegerField()

    def __int__(self):
        return self.status


class StatusServico(models.Model):
    nome = models.CharField(max_length=12)

    def __int__(self):
        return self.nome


class Mensageiro(models.Model):
    nome = models.CharField(max_length=20)

    def __int__(self):
        return self.nome
