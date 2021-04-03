from django import forms
from .models import Mensageiros, Clientes


mensageiros = Mensageiros.objects.all()
clientes = Clientes.objects.all()


class ClienteForm(forms.Form):
    choices = []

    for mensageiro in mensageiros:
        choices.append((mensageiro.id, mensageiro.nome,))
    MENSAGEIROS = tuple(choices)

    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        label='Nome'
    )

    contato = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'tel'
            }
        ),
        label='Contato'
    )

    flag_mensageiro = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        ),
        required=False,
        label='Mensageiro instantâneo'
    )

    mensageiro = forms.ChoiceField(
        choices=MENSAGEIROS,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),
        required=False,
        label='Mensageiro'
    )


class ServicosForm(forms.Form):
    choices = []

    for cliente in clientes:
        choices.append((cliente.id, cliente.nome,))
    CLIENTES = tuple(choices)

    tipo = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        label='Tipo'
    )

    valor = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        label='Valor'
    )

    data = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        label='Data'
    )

    pago = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'required': False}
        ),
        required=False,
        label='Pago'
    )

    cliente = forms.ChoiceField(
        choices=CLIENTES,
        widget=forms.Select(
            attrs={'class': 'form-select', 'required': True}
        ),
        required=True,
        label='Cliente'
    )
