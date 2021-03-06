from django import forms
from servicos import models


class ClienteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)

        mensageiros = models.Mensageiro.objects.all().order_by('nome')

        choices = [('', 'Selecione')]

        for mensageiro in mensageiros:
            choices.append((mensageiro.id, mensageiro.nome,))
        MENSAGEIROS = tuple(choices)

        self.fields['mensageiro'].choices = MENSAGEIROS
    
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
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),
        required=False,
        label='Mensageiro'
    )


class ServicoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ServicoForm, self).__init__(*args, **kwargs)
        
        clientes = models.Cliente.objects.all().order_by('nome')

        choices = []

        for cliente in clientes:
            choices.append((cliente.id, cliente.nome,))
        CLIENTES = tuple(choices)

        self.fields['cliente'].choices = CLIENTES

        status = models.StatusServico.objects.all().order_by('nome')

        choices = [('', 'Selecione')]

        for stat in status:
            choices.append((stat.id, stat.nome,))
        STATUS = tuple(choices)

        self.fields['status'].choices = STATUS

    tipo = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        label='Tipo'
    )

    valor = forms.CharField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': '0.01'}
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
        widget=forms.Select(
            attrs={'class': 'form-select', 'required': True}
        ),
        required=True,
        label='Cliente'
    )

    status = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-select', 'required': True}
        ),
        required=True,
        label='Status'
    )