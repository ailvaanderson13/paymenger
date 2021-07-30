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
}

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
                            confirmButtonColor: '#60B532',
                            confirmButtonText: 'Fechar!',
                            html: `
                                <div class="modal-body">
                                    <div class="row">
                                        <div class="col text-left">
                                            <h4><b>Valor da Parcela: </b>R$: ${data.parcela.toFixed(2)}</h4>
                                            <h4><b>Valor Total: </b>R$: ${data.valor_total.toFixed(2)}</h4>
                                            <h4><b>Lucro: </b>R$: ${data.valor_juros.toFixed(2)}</h4>
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
}

