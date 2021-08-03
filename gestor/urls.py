from django.contrib import admin
from django.urls import path, include
from apps.utils.views import login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.utils.urls', 'utils'), namespace='utils')),
    path('agiota/', include(('apps.agiota.urls', 'agiota'), namespace='agiota')),
    path('cliente/', include(('apps.cliente.urls', 'cliente'), namespace='cliente')),
    path('emprestimo/', include(('apps.emprestimo.urls', 'emprestimo'), namespace='emprestimo')),
]
