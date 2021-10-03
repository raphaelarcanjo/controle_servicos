from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.messages import constants as message_constants
from . import models, forms
from datetime import datetime

# Create your views here.


def index(request):
    return render(request, 'home.html')


def adicionarCliente(request):
    if request.method == 'POST':
        form = forms.ClienteForm(request.POST)
        if form.is_valid():
            cliente = models.Cliente()
            mensageiro = models.Mensageiro.objects.get(id=request.POST.get('mensageiro'))
            cliente.nome = request.POST.get('nome')
            cliente.contato = request.POST.get('contato')
            cliente.flag_mensageiro = True if request.POST.get('flag_mensageiro') else False
            cliente.mensageiro = mensageiro
            cliente.save()

    clientes = models.Cliente.objects.all().select_related('mensageiro')
    form = forms.ClienteForm()

    data = {
        'clientes': clientes,
        'form': form
    }

    return render(request, 'adicionar_cliente.html', data)


def adicionarServico(request):
    if request.method == 'POST':
        form = forms.ServicoForm(request.POST)

        if form.is_valid():
            servico = models.Servico()
            status = models.StatusServico.objects.get(id=request.POST.get('status'))
            servico.tipo = request.POST.get('tipo')
            servico.valor = request.POST.get('valor')
            servico.data = request.POST.get('data')
            servico.pago = 0
            servico.status = status
            servico.save()

            servico = models.Servico.objects.last()
            cliente = models.Cliente.objects.get(id=request.POST.get('cliente'))

            clienteservico = models.ClienteServico()
            clienteservico.cliente = cliente
            clienteservico.servico = servico
            clienteservico.save()

    clientes = models.Cliente.objects.all()
    form = forms.ServicoForm({'data': datetime.now().strftime('%Y-%m-%d')})
    status = models.StatusServico.objects.all()
    clienteservico = models.ClienteServico.objects.all().select_related('servico', 'cliente')
    total = 0
    liquido = 0

    for sc in clienteservico.values_list('servico_id'):
        servico = models.Servico.objects.get(id=sc[0])
        total += float(servico.valor)
        if servico.pago is True:
            liquido += float(servico.valor)

    data = {
        'clientes': clientes,
        'form': form,
        'total': total,
        'liquido': liquido,
        'clienteservico': clienteservico,
        'status': status
    }

    return render(request, 'adicionar_servico.html', data)


def editarServico(request, servico_id):
    if request.method == 'POST':
        form = forms.ServicoForm(request.POST)
        if form.is_valid():
            servico = models.Servico.objects.get(id=servico_id)
            if request.POST.get('status'):
                status = models.StatusServico.objects.get(id=request.POST.get('status'))
            else:
                status = None
            servico.tipo = request.POST.get('tipo')
            servico.valor = request.POST.get('valor')
            servico.data = request.POST.get('data')
            servico.pago = True if request.POST.get('pago') else False
            servico.status = status
            servico.save()

            clienteservico = models.ClienteServico.objects.get(id=request.POST.get('clienteservico_id'))
            clienteservico.cliente = models.Cliente.objects.get(id=request.POST.get('cliente'))
            clienteservico.save()
            return redirect('novoservico')

    try:
        servico = models.Servico.objects.filter(id=servico_id).select_related('status').only('id')
    except:
        messages.error(request, 'Serviço não encontrado')
        return redirect('novoservico')

    clienteservico = models.ClienteServico.objects.get(servico_id=servico_id)
    status = models.StatusServico.objects.all()
    clientes = models.Cliente.objects.all()
    formdata = servico.values().get()
    formdata['status'] = formdata['status_id']
    formdata['cliente'] = clienteservico.cliente_id
    form = forms.ServicoForm(initial=formdata)

    data = {
        'clienteservico': clienteservico,
        'status': status,
        'clientes': clientes,
        'form': form
    }

    return render(request, 'editar_servico.html', data)


def editarCliente(request, cliente_id):
    if request.method == 'POST':
        form = forms.ClienteForm(request.POST)
        if form.is_valid():
            cliente = models.Cliente.objects.get(id=cliente_id)
            if request.POST.get('mensageiro') and request.POST.get('flag_mensageiro'):
                mensageiro = models.Mensageiro.objects.get(id=request.POST.get('mensageiro'))
            else:
                mensageiro = None
            cliente.nome = request.POST.get('nome')
            cliente.contato = request.POST.get('contato')
            cliente.flag_mensageiro = True if request.POST.get('flag_mensageiro') else False
            cliente.mensageiro = mensageiro
            cliente.save()
            return redirect('novocliente')

    try:
        cliente = models.Cliente.objects.filter(id=cliente_id).select_related('mensageiro').only('id').values().get()
    except models.Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado')
        return redirect('home')

    cliente['mensageiro'] = cliente['mensageiro_id']
    form = forms.ClienteForm(initial=cliente)

    data = {
        'form': form,
        'cliente': cliente
    }

    return render(request, 'editar_cliente.html', data)


def removerServico(request, servico_id):
    if request.method == 'POST':
        models.Servico.objects.filter(id=servico_id).delete()
        return redirect('novoservico')

    try:
        servico = models.ClienteServico.objects.filter(servico_id=servico_id).select_related('servico','cliente').get()
    except models.ClienteServico.DoesNotExist:
        messages.error(request, 'Serviço não encontrado')
        return redirect('novoservico')

    # return HttpResponse(servico)
    data = {
        'servico': servico
    }

    return render(request, 'remover_servico.html', data)


def removerCliente(request, cliente_id):
    if request.method == 'POST':
        models.Cliente.objects.filter(id=cliente_id).delete()
        return redirect('novocliente')

    try:
        cliente = models.Cliente.objects.filter(id=cliente_id).select_related('mensageiro').get()
    except models.Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado')
        return redirect('novocliente')

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

def admin(request):
    return render(request, 'admin')

def adicionarMensageiro(request):
    data = {}
    return render(request, 'adicionar_mensageiro', data)

def config(request):
    return render(request, 'config.html')