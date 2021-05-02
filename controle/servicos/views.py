from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.messages import constants as message_constants
from . import models, forms
from datetime import datetime

# Create your views here.


def index(request):
    return render(request, 'home.html')


def adicionarCliente(request):
    clientes = models.Cliente.objects.raw('''
        SELECT servicos_cliente.*,
        servicos_mensageiro.nome AS mensageiro_nome
        FROM servicos_cliente
        LEFT JOIN servicos_mensageiro
        ON servicos_mensageiro.id = servicos_cliente.mensageiro
    ''')
    form = forms.ClienteForm()

    if request.method == 'POST':
        form = forms.ClienteForm(request.POST)
        if form.is_valid():
            cliente = forms.Cliente()
            cliente.nome = request.POST.get('nome')
            cliente.contato = request.POST.get('contato')
            cliente.flag_mensageiro = True if request.POST.get('flag_mensageiro') else False
            cliente.mensageiro = request.POST.get('mensageiro')
            cliente.save()
            return redirect('home')

    data = {
        'clientes': clientes,
        'form': form
    }

    return render(request, 'adicionar_cliente.html', data)


def adicionarServico(request):
    clientes = models.Cliente.objects.all()
    form = forms.ServicoForm({'data': datetime.now().strftime('%Y-%m-%d')})
    status = models.StatusServico.objects.all()
    servicos = models.Servico.objects.all().raw('''
        SELECT *, servicos_cliente.nome, servicos_clienteservico.cliente
        FROM servicos_servico
        LEFT JOIN servicos_clienteservico
        ON servicos_clienteservico.servico = servicos_servico.id
        LEFT JOIN servicos_cliente
        ON servicos_cliente.id = servicos_clienteservico.cliente
        ''')
    total = 0
    liquido = 0

    for servico in servicos:
        total += int(servico.valor)
        if servico.pago is True:
            liquido += int(servico.valor)

    if request.method == 'POST':
        form = forms.ServicoForm(request.POST)

        if form.is_valid():
            servico = models.Servico()
            servico.tipo = request.POST.get('tipo')
            servico.valor = request.POST.get('valor')
            servico.data = request.POST.get('data')
            servico.pago = 0
            servico.status = 1
            servico.save()
            servico = models.Servico.objects.last()

            clienteservico = models.ClienteServico()
            clienteservico.cliente = request.POST.get('cliente')
            clienteservico.servico = servico.id
            clienteservico.save()
            return redirect('home')

    data = {
        'clientes': clientes,
        'form': form,
        'total': total,
        'liquido': liquido,
        'servicos': servicos,
        'status': status
    }

    return render(request, 'adicionar_servico.html', data)


def editarServico(request, servico_id):
    servico = models.Servico.objects.filter(id=servico_id).values()
    if servico:
        servico = servico[0]
    else:
        messages.error(request, 'Serviço não encontrado')
        return redirect('home')
    cliente = models.ClienteServico.objects.filter(servico=servico_id).values()
    if cliente:
        cliente = cliente[0]
    else:
        cliente = None
    status = models.StatusServico.objects.all()
    clientes = models.Cliente.objects.all()
    form = forms.ServicoForm(initial=servico)

    if request.method == 'POST':
        form = forms.ServicoForm(request.POST)
        if form.is_valid():
            servico = models.Servico.objects.get(id=servico_id)
            servico.tipo = request.POST.get('tipo')
            servico.valor = request.POST.get('valor')
            servico.data = request.POST.get('data')
            servico.pago = int(request.POST.get('pago'))
            servico.status = request.POST.get('status')
            servico.save()
            try:
                clienteservico = models.ClienteServico.objects.get(servico=servico_id)
            except models.ClienteServico.DoesNotExist:
                clienteservico = models.ClienteServico()
            clienteservico.cliente = request.POST.get('cliente')
            clienteservico.servico = servico_id
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


def editarCliente(request, cliente_id):
    cliente = models.Cliente.objects.filter(id=cliente_id).values()

    if cliente:
        cliente = cliente[0]
    else:
        messages.error(request, 'Cliente não encontrado')
        return redirect('home')

    form = forms.ClienteForm(initial=cliente)

    if request.method == 'POST':
        if form.is_valid():
            form = forms.ClienteForm(request.POST)
            form.save()
            return redirect('home')

    data = {
        'form': form,
        'cliente': cliente
    }

    return render(request, 'editar_cliente.html', data)


def removerServico(request, servico_id):
    servico = models.Servico.objects.filter(id=servico_id).values()

    if servico:
        servico = servico[0]
    else:
        messages.error(request, 'Serviço não encontrado')
        return redirect('home')

    if request.method == 'POST':
        models.Servico.objects.filter(id=servico_id).delete()
        return redirect('home')

    data = {
        'servico': servico
    }

    return render(request, 'remover_servico.html', data)


def removerCliente(request, cliente_id):
    cliente = models.Cliente.objects.filter(id=cliente_id).values()

    if cliente:
        cliente = cliente[0]
    else:
        messages.error(request, 'Cliente não encontrado')
        return redirect('home')

    if request.method == 'POST':
        models.Cliente.objects.filter(id=cliente_id).delete()
        return redirect('home')

    data = {
        'cliente': cliente
    }

    return render(request, 'remover_cliente.html', data)


def relatorio(request):
    mes = request.GET.get('mes') if request.GET.get('mes') else str(datetime.now().strftime('%m'))
    meses = {
        '01': 'Janeiro',
        '02': 'Fevereiro',
        '03': 'Março',
        '04': 'Abril',
        '05': 'Maio',
        '06': 'Junho',
        '07': 'Julho',
        '08': 'Agosto',
        '09': 'Setembro',
        '10': 'Outubro',
        '11': 'Novembro',
        '12': 'Desembro',
    }

    data = {
        'mes': mes,
        'meses': meses
    }

    return render(request, 'relatorio.html', data)