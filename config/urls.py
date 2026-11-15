"""Rotas principais do projeto Lente Selvagem."""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

# Em produção (Render, com DEBUG desligado) o próprio Django serve os arquivos
# reunidos pelo collectstatic, sem depender de pacotes extras.
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
