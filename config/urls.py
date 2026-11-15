"""Rotas principais do projeto Lente Selvagem."""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
