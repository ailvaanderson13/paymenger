from django.urls import path
from . import views

urlpatterns = [
    path('new-emprestimo/', views.confirm_emprestimo, name="new-emprestimo"),
    path('edit-emprestimo/<int:pk>', views.open_update_emprestimo, name="edit-emprestimo"),
    path('open-emprestimo/', views.open_update_emprestimo, name="open-emprestimo"),
    path('list-emprestimos/', views.list_emprestimos, name="list-emprestimo"),
    path('calc-emprestimo/', views.calc_emprestimo, name="calc-emprestimo"),
]