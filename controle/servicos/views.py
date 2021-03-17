from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from . import models, forms

# Create your views here.


def index(request):
    status = models.StatusServico.objects.all()
    servicos = models.Servicos.objects.all().raw('''
        SELECT *, servicos_clientes.nome
        FROM servicos_servicos
        LEFT JOIN servicos_clienteservico
        ON servicos_clienteservico.servico = servicos_servicos.id
        LEFT JOIN servicos_clientes
        ON servicos_clientes.id = servicos_clienteservico.cliente
        ''')
    total = 0
    liquido = 0

    for servico in servicos:
        total += int(servico.valor)
        if servico.pago is True:
            liquido += int(servico.valor)

    data = {
        'total': total,
        'liquido': liquido,
        'servicos': servicos,
        'status': status
    }

    return render(request, 'home.html', data)


def adicionarCliente(request):
    form = forms.ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('home')

    data = {
        'form': form
    }

    return render(request, 'adicionar_cliente.html', data)


def adicionarServico(request):
    clientes = models.Clientes.objects.all()
    form = forms.ServicosForm(request.POST or None)

    if form.is_valid():
        servico = form.save()
        clienteservico = models.ClienteServico()
        clienteservico.cliente = request.POST.get('cliente')
        clienteservico.servico = servico
        clienteservico.save()
        return redirect('home')

    data = {
        'clientes': clientes,
        'form': form
    }

    return render(request, 'adicionar_servico.html', data)


def editarServico(request, servico_id):
    servico = models.Servicos.objects.get(id=servico_id)
    try:
        cliente = models.ClienteServico.objects.get(servico=servico_id)
    except models.ClienteServico.DoesNotExist:
        cliente = None
    status = models.StatusServico.objects.all()
    clientes = models.Clientes.objects.all()
    form = forms.ServicosForm(request.POST, initial=model_to_dict(servico))

    if request.POST:
        if form.is_valid():
            servico = form.save()
            clienteservico = models.ClienteServico()
            clienteservico.cliente = request.POST.get('cliente')
            clienteservico.servico = servico
            clienteservico.save()
            return redirect('home')

    data = {
        'servico': servico,
        'status': status,
        'clientes': clientes,
        'servico_cliente': cliente,
        'form': form
    }

    return render(request, 'editar_servico.html', data)
