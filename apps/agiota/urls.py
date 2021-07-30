from django.urls import path
from . import views


urlpatterns = [
    path('list-agiota/', views.list_agiotas, name="list_agiotas"),
    path('new-agiota/', views.create_update_agiota, name="new_agiota"),
    path('edit-agiota/<int:pk>', views.create_update_agiota, name="edit_agiota"),
]