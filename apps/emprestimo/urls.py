from django.urls import path
from . import views

urlpatterns = [
    path('new-emprestimo/', views.create_update_emprestimo, name="new-emprestimo"),
    path('edit-emprestimo/<int:pk>', views.create_update_emprestimo, name="edit-emprestimo"),
    path('list-emprestimos/', views.list_emprestimos, name="list-emprestimo"),
    path('calc-emprestimo/', views.calc_emprestimo, name="calc-emprestimo"),
]