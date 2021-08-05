$('#btn-calcular').on('click', function (){
    validate_required();
});

function validate_required (){
    let ok = true
    $('.req').each(function (){
        if ($(this).val() == '' || $(this).val() == '0' || $(this).val() == 0){
            ok = false;
            Swal.fire({
                title: 'Oops!',
                html: `Preencha o campo de <b>${$(this).attr('name')}</b>!`,
                icon: 'error',
                timer: 3000,
                showConfirmButton: false,
            })
        }
    })
    if (ok){
        get_send_data()
    }
};

function get_send_data(){
var valor = $('#id_valor').val();
var juros = $('#id_juros').val();
var parcela = $('#id_parcela').val();

    if(valor && juros && parcela){
        $.ajax({
            'url': '/emprestimo/calc-emprestimo/',
            'type': 'POST',
            'dataType': 'json',
            'data': {
                'valor': valor,
                'juros': juros,
                'parcela': parcela,
            },
            success: function (data) {
                if (data.success) {
                    if (data.parcela || data.valor_total || data.valor_juros){
                        Swal.fire({
                            title: 'Informações do Empréstimo!',
                            showConfirmButton: false,
                            html: `
                                <div class="modal-body">
                                    <div class="row">
                                        <div class="col text-left">
                                            <h4><b>Qtd. Parcelas: </b>${parcela}x</h4>
                                            <h4><b>Valor da Parcela: </b>R$: ${data.parcela.toFixed(2).replace('.', ',')}</h4>
                                            <h4><b>Valor Total: </b>R$: ${data.valor_total.toFixed(2).replace('.', ',')}</h4>
                                            <h4><b>Lucro: </b>R$: ${data.valor_juros.toFixed(2).replace('.', ',')}</h4>
                                        </div>
                                    </div>
                                    <br>
                                    <div class="row">
                                        <div class="col">
                                            <button id="btn-fechar" onclick="swal.closeModal()" class="btn btn-danger text-white">Fechar!</button>
                                        </div>
                                        <div class="col">
                                            <button id="btn-contratar" onclick="contratar()" class="btn btn-success text-white">Contratar!</button>
                                        </div>
                                    </div>
                                </div>
                            `
                        })
                    }
                }
            }
        })
    }
};

function contratar(){
    Swal.fire({
      title: 'Tem certeza?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sim'
      cancelButtonText: 'Não'
    }).then((result) => {
        if (result.isConfirmed) {
            let client = $('#id_cliente').val();
            let valor = $('#id_valor').val();
            let juros = $('#id_juros').val();
            let parcela = $('#id_parcela').val();
            let vencimento = $('#id_vencimento').val();
            var pk = $('.cls-pk').val();
            var csrf = $('input[name=csrfmiddlewaretoken]').val();
            $.ajax({
                'url': '/emprestimo/new-emprestimo/',
                'type': 'POST',
                'dataType': 'json',
                 'data' : {
                        'cliente': client,
                        'valor': valor,
                        'juros': juros,
                        'parcela': parcela,
                        'vencimento': vencimento,
                        'pk_': pk,
                        csrfmiddlewaretoken: csrf,
                 },
                success: function (data){
                    if (data.success && data.edit ){
                        Swal.fire({
                            position: 'center',
                            icon: 'success',
                            title: 'Empréstimo Editado com Sucesso!',
                            allowOutsideClick: false,
                            allowEscapeKey: false,
                        }).then((result) => {
                            if (result.value) {
                                location.reload();
                            }
                        });
                    } else if(data.success){
                        Swal.fire({
                            position: 'center',
                            icon: 'success',
                            title: 'Empréstimo Contratado com Sucesso!',
                            allowOutsideClick: false,
                            allowEscapeKey: false,
                        }).then((result) => {
                            if (result.value) {
                                location.reload();
                            }
                        });
                    } else {
                         Swal.fire({
                          position: 'center',
                          icon: 'error',
                          title: 'Algo de errado!',
                          showConfirmButton: false,
                          timer: 1500
                        })
                    }
                }
            })
        }
    })
}

$('.btn-detail').on('click', function(){
    let pk = $(this).val();
    if (pk){
        $.ajax({
            'url': '/emprestimo/detail-emprestimo/',
            'type': 'POST',
            'dataType': 'json',
            'data' : {
                'pk': pk,
            },
            success: function(data){
                if (data.success){
                    Swal.fire({
                        title: 'Detalhes do Empréstimo!',
                        showConfirmButton: true,
                        confirmButtonColor: '#3085d6',
                        html: `
                        <div class="modal-body">
                            <div class="row">
                                <div class="col text-left">
                                    <h4><b>Cliente: </b>${data.cliente}</h4>
                                    <h4><b>Valor inicial: </b>${data.valor_inicial.toFixed(2).replace('.', ',')}</h4>
                                    <h4><b>Qtd. Parcelas: </b>${data.qtd_parcela.toFixed(0)}x</h4>
                                    <h4><b>Valor da Parcela: </b>R$: ${data.valor_parcela.toFixed(2).replace('.', ',')}</h4>
                                    <h4><b>Taxa de juros: </b>${data.taxa_juros}%</h4>
                                    <h4><b>Valor Total: </b>R$: ${data.valor_total.toFixed(2).replace('.', ',')}</h4>
                                    <h4 class="text-success"><b>Lucro: </b>R$: ${data.valor_juros.toFixed(2).replace('.', ',')}</h4>
                                </div>
                            </div>
                        </div>`
                    })
                }
            }
        })
    }
});

$('.btn-pagou').on('click', function (){
    Swal.fire({
      title: 'Confirma Pagamento da Parcela?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sim'
    }).then((result) => {
        if (result.isConfirmed) {
            let pk = $(this).attr('pk');
            if (pk){
                $.ajax({
                    'url': '/emprestimo/update-payment/',
                    'type': 'POST',
                    'dataType': 'json',
                    'data' : {
                        'pk': pk,
                    },
                    success: function(data){
                        console.log(data)
                        if (data.success){
                            Swal.fire({
                                position: 'center',
                                icon: 'success',
                                title: 'Status de Pagamento Atualizado!',
                                allowOutsideClick: false,
                                allowEscapeKey: false,
                            }).then((result) => {
                                if (result.value) {
                                    location.reload();
                                }
                            });
                        } else if (data.success || data.quitou){
                            Swal.fire({
                                position: 'center',
                                icon: 'success',
                                title: 'Última parcela! Emprestimo Quitado!',
                                allowOutsideClick: false,
                                allowEscapeKey: false,
                            }).then((result) => {
                                if (result.value) {
                                    location.reload();
                                }
                            });
                        }
                    }
                })
            }
        }
    })
})

