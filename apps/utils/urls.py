from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login/', views.acesso, name="login"),
    path('logout/', views.logout_, name="logout"),
]

