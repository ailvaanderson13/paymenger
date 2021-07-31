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
                                            <h4><b>Valor da Parcela: </b>R$: ${data.parcela.toFixed(2)}</h4>
                                            <h4><b>Valor Total: </b>R$: ${data.valor_total.toFixed(2)}</h4>
                                            <h4><b>Lucro: </b>R$: ${data.valor_juros.toFixed(2)}</h4>
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
      title: 'Tem certeza que quer contratar?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sim'
    }).then((result) => {
        if (result.isConfirmed) {
            let cliente = $('#id_cliente').val();
            console.log(cliente)
            $.ajax({
                'url': '/emprestimo/new-emprestimo/',
                'type': 'POST',
                'dataType': 'json',
                 'data' : {
                        'ok': 'ok',
                        'pk': cliente
                 },
                success: function (data){
                    if (data.success){
                        Swal.fire({
                          position: 'center',
                          icon: 'success',
                          title: 'Empréstimo contratado!',
                          showConfirmButton: false,
                          timer: 1500
                        })
                    }
                }
            })
        }
    })
}

