from django.shortcuts import render, redirect
from . import models, forms

# Create your views here.


def index(request):
    status = models.StatusServico.objects.all()
    servicos = models.Servicos.objects.all().raw('''
        SELECT *, servicos_clientes.nome, servicos_clienteservico.cliente
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

    if request.method == 'POST':
        if form.is_valid():
            form = forms.ClienteForm(request.POST)
            form.save()
            return redirect('home')

    data = {
        'form': form
    }

    return render(request, 'adicionar_cliente.html', data)


def adicionarServico(request):
    clientes = models.Clientes.objects.all()
    form = forms.ServicosForm()

    if request.method == 'POST':
        form = forms.ServicosForm(request.POST)

        if form.is_valid():
            print('ok')
            servico = models.Servicos()
            servico.tipo = request.POST.get('tipo')
            servico.valor = request.POST.get('valor')
            servico.data = request.POST.get('data')
            servico.pago = 0
            servico.status = 1
            servico.save()
            servico = models.Servicos.objects.last()

            clienteservico = models.ClienteServico()
            clienteservico.cliente = request.POST.get('cliente')
            clienteservico.servico = servico.id
            clienteservico.save()
            return redirect('home')

    data = {
        'clientes': clientes,
        'form': form
    }

    return render(request, 'adicionar_servico.html', data)


def editarServico(request, servico_id):
    try:
        servico = models.Servicos.objects.filter(id=servico_id).values()[0]
    except models.Servicos.IndexError:
        return redirect('home')
    try:
        cliente = models.ClienteServico.objects.filter(servico=servico_id).first()
    except models.ClienteServico.DoesNotExist:
        cliente = None
    status = models.StatusServico.objects.all()
    clientes = models.Clientes.objects.all()
    form = forms.ServicosForm(initial=servico)

    if request.method == 'POST':
        form = forms.ServicosForm(request.POST)
        if form.is_valid():
            servico = models.Servicos.objects.get(id=servico_id)
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
    try:
        cliente = models.Clientes.objects.filter(id=cliente_id).values()[0]
    except models.Clientes.IndexError:
        redirect('home')
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