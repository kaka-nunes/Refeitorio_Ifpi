from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static

from dining_hall import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dining_hall.accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Refeitório - IFPI"
admin.site.site_title = "Sistema de Administração do Refeitório - IFPI"
admin.site.index_title = "Refeitório - IFPI"