from django.urls import path
from . import views


urlpatterns = [
    path('create-cliente/', views.create_update_cliente, name="create-cliente"),
    path('edit-cliente/<int:pk>', views.create_update_cliente, name="edit-cliente"),
    path('list-clientes/', views.list_clientes, name="list-clientes"),
    path('delete-cliente/', views.delete_cliente, name="delete-cliente")
]
