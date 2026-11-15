"""
Popula o banco com os dados de exemplo da parte 4.

Uso:
    python manage.py popular_banco           # cria o que ainda não existe
    python manage.py popular_banco --limpar  # apaga posts, comentários e categorias antes
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from blog.dados_exemplo import CATEGORIAS, POSTS, USUARIOS
from blog.models import Category, Comment, Post


class Command(BaseCommand):
    help = 'Popula o banco com posts, categorias, usuários e comentários de exemplo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpar', action='store_true',
            help='Apaga todos os posts, comentários e categorias antes de popular.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['limpar']:
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write('Posts, comentários e categorias apagados.')

        categorias = {}
        for nome, descricao in CATEGORIAS:
            categorias[nome], _ = Category.objects.get_or_create(
                name=nome, defaults={'description': descricao},
            )

        User = get_user_model()
        usuarios = {}
        for username, nome, sobrenome in USUARIOS:
            user, criado = User.objects.get_or_create(
                username=username, defaults={'first_name': nome, 'last_name': sobrenome},
            )
            if criado:
                # Usuários de exemplo não fazem login
                user.set_unusable_password()
                user.save()
            usuarios[username] = user

        novos = 0
        for dados in POSTS:
            post, criado = Post.objects.get_or_create(
                title=dados['title'],
                defaults={'content': dados['content'], 'pub_date': dados['pub_date']},
            )
            if not criado:
                self.stdout.write(f'Já existe, mantido: {post.title}')
                continue
            novos += 1
            post.categories.set(categorias[nome] for nome in dados['categories'])
            for username, texto, data in dados['comments']:
                Comment.objects.create(
                    post=post, author=usuarios[username], text=texto, pub_date=data,
                )

        self.stdout.write(self.style.SUCCESS(
            f'Pronto: {novos} post(s) novo(s). Total no banco: '
            f'{Post.objects.count()} posts, {Comment.objects.count()} comentários, '
            f'{Category.objects.count()} categorias.'
        ))
