from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import models, forms


def create_update_emprestimo(request, pk=None):
    firma = request.user.firma.pk
    page_title = "Abertura de Empréstimo" if not pk else "Editar Empréstimo"
    msg = None
    notification = None
    form = forms.EmprestimoForm()
    emprestimo = None

    if pk:
        emprestimo = models.Emprestimo.objects.filter(is_active=True)
        if emprestimo:
            emprestimo = emprestimo.last()
            form = forms.EmprestimoForm(instance=emprestimo)
        else:
            msg="Nenhum Empréstimo encontrado!"
            notification = "danger"

    if request.method == "POST":
        if emprestimo:
            form = forms.EmprestimoForm(request.POST, instance=emprestimo)
        else:
            form = forms.EmprestimoForm(request.POST)

        try:
            if form.is_valid():
                if emprestimo:
                    form.save()
                    msg = "Atualização Salva com Sucesso!"
                    notification = "success"
                else:
                    new_emprestimo = form.save(commit=False)
                    new_emprestimo.firma_id = firma
                    form.save()
                    msg = "Empréstimo Salvo com Sucesso!"
                    notification = "success"
        except Exception as e:
            msg = e
            notification = "warning"

    context = {
       'page_title': page_title, 'msg': msg, 'notification': notification, 'form': form
    }

    return render(request, 'cadastro_emprestimo.html', context)


def list_emprestimos(request):
    page_title = "Empréstimos Cadastrados"
    msg = None
    notification = None

    emprestimos = models.Emprestimo.objects.filter(is_active=True, firma=request.user.firma)

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













