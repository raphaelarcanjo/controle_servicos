from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from servicos import models, forms
from datetime import datetime


class HomeView:
    def index(request):
        return render(request, 'home.html')

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

    def config(request):
        data = {
            'mensageiros': models.Mensageiro.objects.all(),
            'status': models.StatusServico.objects.all()
        }

        return render(request, 'config.html', data)

class ClienteView:
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
                return redirect('cliente:novocliente')

        try:
            cliente = models.Cliente.objects.filter(id=cliente_id).select_related('mensageiro').only('id').values().get()
        except models.Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado')
            return redirect('home:home')

        cliente['mensageiro'] = cliente['mensageiro_id']
        form = forms.ClienteForm(initial=cliente)

        data = {
            'form': form,
            'cliente': cliente
        }

        return render(request, 'editar_cliente.html', data)

    def removerCliente(request, cliente_id):
        if request.method == 'POST':
            models.Cliente.objects.filter(id=cliente_id).delete()
            return redirect('cliente:novocliente')

        try:
            cliente = models.Cliente.objects.filter(id=cliente_id).select_related('mensageiro').get()
        except models.Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado')
            return redirect('cliente:novocliente')

        data = {
            'cliente': cliente
        }

        return render(request, 'remover_cliente.html', data)


class ServicoView:
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
                return redirect('servico:novoservico')

        try:
            servico = models.Servico.objects.filter(id=servico_id).select_related('status').only('id')
        except:
            messages.error(request, 'Serviço não encontrado')
            return redirect('servico:novoservico')

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

    def removerServico(request, servico_id):
        if request.method == 'POST':
            models.Servico.objects.filter(id=servico_id).delete()
            return redirect('servico:novoservico')

        try:
            servico = models.ClienteServico.objects.filter(servico_id=servico_id).select_related('servico','cliente').get()
        except models.ClienteServico.DoesNotExist:
            messages.error(request, 'Serviço não encontrado')
            return redirect('servico:novoservico')

        data = {
            'servico': servico
        }

        return render(request, 'remover_servico.html', data)


class ConfigView:
    def adicionarMensageiro(request):
        mensageiro = {'nome': request.POST.get('nome')}
        if request.method == 'POST':
            if not request.POST.get('nome'):
                messages.error(request, 'O campo nome deve ser preenchido')
                return redirect('config:adicionarmensageiro')
            mensageiro = models.Mensageiro()
            mensageiro.nome = request.POST.get('nome')
            mensageiro.save()
            return redirect('home:config')
        data = {
            'mensageiro': mensageiro
        }
        return render(request, 'adicionar_mensageiro.html', data)

    def removerMensageiro(request, mensageiro_id):
        if request.method == 'POST':
            models.Mensageiro.objects.filter(id=mensageiro_id).delete()
            return redirect('home:config')
        
        try:
            mensageiro = models.Mensageiro.objects.get(id=mensageiro_id)
        except models.Mensageiro.DoesNotExist:
            messages.error(request, 'Mensageiro não encontrado')
            return redirect('home:config')
        data = {
            'mensageiro': mensageiro
        }
        return render(request, 'remover_mensageiro.html', data)

    def adicionarStatus(request):
        status = {'nome': request.POST.get('nome')}
        if request.method == 'POST':
            if not request.POST.get('nome'):
                messages.error(request, 'O campo nome deve ser preenchido')
                return redirect('config:adicionarstatus')
            status = models.StatusServico()
            status.nome = request.POST.get('nome')
            status.save()
            return redirect('home:config')
        data = {
            'status': status
        }
        return render(request, 'adicionar_status.html', data)

    def removerStatus(request, status_id):
        if request.method == 'POST':
            models.StatusServico.objects.filter(id=status_id).delete()
            return redirect('home:config')
        
        try:
            status = models.StatusServico.objects.get(id=status_id)
        except models.StatusServico.DoesNotExist:
            messages.error(request, 'Status não encontrado')
            return redirect('home:config')
        data = {
            'status': status
        }
        return render(request, 'remover_status.html', data)