from django import forms
from . import models


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Clientes

        mensageiros = models.Mensageiros.objects.all()
        choices = []

        for mensageiro in mensageiros:
            choices.append((mensageiro.id, mensageiro.nome,))
        CHOICES = tuple(choices)

        fields = (
            'nome',
            'contato',
            'flag_mensageiro',
            'mensageiro',
        )

        widgets = {
            'nome': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'contato': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'tel'
                }
            ),
            'flag_mensageiro': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'mensageiro': forms.Select(
                attrs={'type': 'date', 'class': 'form-select'},
                choices=CHOICES
            ),
        }

        labels = {
            'nome': 'Nome',
            'contato': 'Contato',
            'flag_mensageiro': 'Mensageiro instantâneo',
            'mensageiro': 'Mensageiro',
        }


class ServicosForm(forms.ModelForm):
    class Meta:
        model = models.Servicos

        fields = (
            'tipo',
            'valor',
            'data',
            'pago',
        )

        widgets = {
            'tipo': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'valor': forms.TextInput(
                attrs={
                    'type': 'number',
                    'min': '0.00',
                    'step': '0.01',
                    'class': 'form-control'
                }
            ),
            'data': forms.TextInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'pago': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

        labels = {
            'tipo': 'Tipo',
            'valor': 'Valor:',
            'data': 'Data',
            'pago': 'Pago',
        }


class StatusServicoForm(forms.ModelForm):
    class Meta:
        model = models.StatusServico

        fields = ('nome',)

        widgets = {
            'nome': forms.RadioSelect(
                attrs={'class': 'form-check-input'}
            )
        }

        labels = {
            'nome': 'Status'
        }
