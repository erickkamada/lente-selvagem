# Lente Selvagem

Blog de fotografia da natureza feito com Django, sem extensões de terceiros. Permite criar, editar e remover posts pela própria página, comentar nos posts e navegar por categorias.

## Como rodar no seu computador

Requer Python 3.10 ou mais recente.

**Windows (PowerShell ou Prompt de Comando)**

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py popular_banco
python manage.py createsuperuser
python manage.py runserver
```

**Linux ou macOS**

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py popular_banco
python manage.py createsuperuser
python manage.py runserver
```

Depois abra http://127.0.0.1:8000/ no navegador. O administrador fica em http://127.0.0.1:8000/admin/.

O comando `popular_banco` cria 4 posts, 4 categorias, 3 usuários (marina, rafael e lucia) e 7 comentários. Ele pode ser rodado de novo sem duplicar nada; com `--limpar`, apaga posts, comentários e categorias e recria tudo.

Para conferir se está tudo funcionando:

```
python manage.py test
```

## Páginas

| Página | URL | Nome da URL |
| --- | --- | --- |
| Listagem de posts | `/` | `blog:post_list` |
| Post individual | `/post/<id>/` | `blog:post_detail` |
| Criar post | `/post/novo/` | `blog:post_create` |
| Editar post | `/post/<id>/editar/` | `blog:post_update` |
| Remover post (confirmação) | `/post/<id>/remover/` | `blog:post_delete` |
| Criar comentário | `/post/<id>/comentar/` | `blog:comment_create` |
| Listagem de categorias | `/categorias/` | `blog:category_list` |
| Categoria individual | `/categorias/<id>/` | `blog:category_detail` |

## Consultas SQL

As cinco consultas da parte 4 estão em `sql/consultas.sql`. Abra o `db.sqlite3` no DB Browser for SQLite, vá na aba "Executar SQL" e rode uma consulta por vez.

## Implantação no Render

1. Envie o repositório para o GitHub.
2. No Render, crie um **Web Service** a partir do repositório, com:
   - Build Command: `bash build.sh`
   - Start Command: `python -m gunicorn config.wsgi:application`
   - Variável de ambiente `SECRET_KEY` com um valor aleatório.
3. Opcional: defina `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` e `DJANGO_SUPERUSER_PASSWORD` para o build criar o superusuário.

Também dá para usar o arquivo `render.yaml` em **New > Blueprint**. No plano gratuito o disco é temporário: o banco é recriado com os dados de exemplo a cada implantação.

## Histórico do repositório

- `main`: três commits seguidos com as três versões das views (funções sem forms, funções com form, classes genéricas).
- `comments`: modelo `Comment` e criação de comentários, com merge na `main`.
- `categories`: modelo `Category` e páginas de categorias, criado a partir da `main` depois do merge anterior, com merge na `main`.

## Créditos das fotos

As fotos dos posts de exemplo vêm do Wikimedia Commons, e cada legenda leva à página do arquivo, com autoria e licença.
