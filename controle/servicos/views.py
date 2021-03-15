from django.shortcuts import render, redirect
from . import models, forms

# Create your views here.


def index(request):
    servicos = models.Servicos.objects.all()

    data = {
        'servicos': servicos
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
    form = forms.ServicosForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('home')

    data = {
        'form': form
    }

    return render(request, 'adicionar_servico.html', data)
