from django.urls import path
from . import views

urlpatterns = [
    path('new-emprestimo/', views.confirm_emprestimo, name="new-emprestimo"),
    path('edit-emprestimo/<int:pk>', views.open_update_emprestimo, name="edit-emprestimo"),
    path('open-emprestimo/', views.open_update_emprestimo, name="open-emprestimo"),
    path('list-emprestimos/', views.list_emprestimos, name="list-emprestimo"),
    path('calc-emprestimo/', views.calc_emprestimo, name="calc-emprestimo"),
    path('detail-emprestimo/', views.detail_emprestimo, name="detail-emprestimo"),
    path('cobranca-diaria/', views.table_charge, name="cobranca-diaria"),
    path('update-payment/', views.update_status_payment, name="update-payment"),
    path('quitados/', views.emprestimos_quitados, name="emprestimos-quitados"),
]