#!/usr/bin/env bash
# Build do Render: instala dependências, reúne os estáticos e prepara o banco.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py popular_banco

# Cria o superusuário se as variáveis DJANGO_SUPERUSER_* estiverem definidas no Render
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --no-input || true
fi
