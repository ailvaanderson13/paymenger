from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import models, forms


def confirm_emprestimo(request):
    response = {
        'success': False
    }

    if request.method == "POST":
        firma = request.user.firma
        cliente = request.POST.get('cliente')
        valor = request.POST.get('valor')
        juros = request.POST.get('juros')
        parcela = request.POST.get('parcela')
        vencimento = request.POST.get('vencimento')

        if cliente and valor and juros and parcela and vencimento:
            new_emprestimo = models.Emprestimo.objects.create(valor=valor, juros=juros,
                                                              parcela=parcela, vencimento=vencimento,
                                                              firma=firma if firma else None)
            new_emprestimo.cliente_id = int(cliente)
            new_emprestimo.save()
            response = {
                'success': True
            }

    return JsonResponse(response, safe=True)


def open_update_emprestimo(request, pk=None):
    page_title = "Abertura de Empréstimo" if not pk else "Editar Empréstimo"
    msg = None
    notification = None
    form = forms.EmprestimoForm()
    emprestimo = None

    if pk:
        emprestimo = models.Emprestimo.objects.filter(pk=pk, is_active=True)
        if emprestimo:
            emprestimo = emprestimo.last()
            form = forms.EmprestimoForm(instance=emprestimo)
        else:
            msg = "Nenhum Empréstimo encontrado!"
            notification = "danger"

    if request.method == "POST":

        if emprestimo:
            form = forms.EmprestimoForm(request.POST, instance=emprestimo)

        try:
            if form.is_valid():
                if emprestimo:
                    form.save()
                    msg = "Atualização Salva com Sucesso!"
                    notification = "success"
                    form = forms.EmprestimoForm()
        except Exception as e:
            msg = e
            notification = "warning"

    context = {
       'page_title': page_title, 'msg': msg, 'notification': notification, 'form': form, 'emprestimo': emprestimo
    }

    return render(request, 'cadastro_emprestimo.html', context)


def list_emprestimos(request):
    page_title = "Empréstimos Cadastrados"
    msg = None
    notification = None

    emprestimos = models.Emprestimo.objects.filter(is_active=True).order_by('data')

    if not emprestimos:
        msg = "Nenhum Empréstimo em Aberto"
        notification = "danger"

    context = {
        'page_title': page_title, 'msg': msg, 'notification': notification, 'emprestimos': emprestimos
    }

    return render(request, 'emprestimos_cadastrados.html', context)


@csrf_exempt
def calc_emprestimo(request):
    response = {
        'success': False
    }

    if request.method == "POST":

        valor_inicial = request.POST.get('valor')
        juros = request.POST.get('juros')
        meses = request.POST.get('parcela')

        if juros and meses and valor_inicial:
            juros = int(juros)
            meses = int(meses)
            valor_inicial = int(valor_inicial)

            juros = juros / 100

            x = ((1+juros)**meses)-1
            y = (juros*((1+juros)**meses))

            percentual = x/y
            parcela = valor_inicial / percentual
            valor_total = parcela * meses
            valor_juros = valor_total - valor_inicial

            response = {
                'success': True,
                'parcela': parcela,
                'valor_total': valor_total,
                'valor_juros': valor_juros,
            }

    return JsonResponse(response, safe=False)