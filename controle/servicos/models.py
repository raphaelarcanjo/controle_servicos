from django.db import models

# Create your models here.


class Clientes(models.Model):
    nome = models.CharField(max_length=80)
    contato = models.CharField(max_length=(20))
    flag_mensageiro = models.BooleanField()
    mensageiro = models.CharField(max_length=(20))

    def __int__(self):
        return self.id


class Servicos(models.Model):
    tipo = models.CharField(max_length=80)
    valor = models.FloatField()
    data = models.DateField()
    pago = models.BooleanField(default=0)
    status = models.IntegerField(default=1)

    def __int__(self):
        return self.id


class ClienteServico(models.Model):
    cliente = models.IntegerField()
    servico = models.IntegerField()


class Andamento(models.Model):
    servico = models.IntegerField()
    status = models.IntegerField()


class StatusServico(models.Model):
    nome = models.CharField(max_length=12)

    def __int__(self):
        return self.id


class Mensageiros(models.Model):
    nome = models.CharField(max_length=20)

    def __int__(self):
        return self.id
