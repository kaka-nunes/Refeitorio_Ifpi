from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]
admin.site.site_header = "Refeitório - IFPI"
admin.site.site_title = "Sistema de Administração do Refeitório - IFPI"
admin.site.index_title = "Refeitório - IFPI"