from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from . import models, forms


def create_update_cliente(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('utils:acesso')

    firma = request.user.firma.pk
    page_title = "Cadastrar Cliente" if not pk else "Editar Cliente"
    form = forms.ClienteForm() if not firma else forms.ClienteAgiotaForm()
    msg = None
    notification = None
    cliente = None

    if pk:
        cliente = models.Cliente.objects.filter(pk=pk)
        if cliente:
            cliente = cliente.last()
            form = forms.ClienteForm(instance=cliente) if not firma else forms.ClienteAgiotaForm(instance=cliente)
        else:
            msg = "Nenhum Cliente Encontrado!"
            notification = 'danger'
    if request.method == "POST":
        if cliente:
            form = forms.ClienteForm(request.POST, instance=cliente)\
                if not firma else forms.ClienteAgiotaForm(request.POST, instance=cliente)
        else:
            form = forms.ClienteForm(request.POST)\
                if not firma else forms.ClienteAgiotaForm(request.POST)

        try:
            if form.is_valid():
                if cliente:
                    cliente.save()
                    msg = "Cadastro Atualizado com Sucesso!"
                    notification = 'success'
                else:
                    if firma:
                        new_cliente = form.save(commit=False)
                        new_cliente.firma_id = firma
                        new_cliente.save()
                        msg = "Cliente cadastrado com Sucesso!"
                        notification = 'success'
            else:
                print(form.errors)
        except Exception as e:
            msg = e
            notification = 'warning'

        form = forms.ClienteForm() if not firma else forms.ClienteAgiotaForm()

    context = {
        'page_title': page_title, 'form': form, 'msg': msg, 'notification': notification
    }

    return render(request, 'cadastro_cliente.html', context)


def list_clientes(request):
    if not request.user.is_authenticated:
        return redirect('utils:acesso')
    page_title = "Clientes Cadastrados"
    msg = None
    notification = None

    if request.user.is_superuser:
        clientes = models.Cliente.objects.filter(is_active=True)
    else:
        clientes = models.Cliente.objects.filter(is_active=True, firma=request.user.firma)

    if not clientes:
        msg = "Nenhum cliente Cadastrado!"
        notification = 'danger'

    context = {
        'page_title': page_title, 'clientes': clientes, 'msg': msg, 'notification': notification
    }

    return render(request, 'clientes_cadastrados.html', context)


@csrf_exempt
def delete_cliente(request):
    if not request.user.is_authenticated:
        return redirect('utils:acesso')
    response = {
        'success': False
    }

    if request.method == 'POST':
        pk = request.POST.get('pk')

        if pk:
            cliente = models.Cliente.objects.get(pk=pk)
            if cliente:
                cliente.is_active = False
                cliente.save()
                response['success'] = True
    return JsonResponse(response, safe=False)