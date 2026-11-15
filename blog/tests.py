"""
Testes do blog. Rode com:  python manage.py test
"""
from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Comment, Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('leitora', password='senha-de-teste-123')
        cls.category = Category.objects.create(name='Paisagens', description='Montanhas e vales.')
        cls.post = Post.objects.create(title='Serra ao amanhecer', content='<p>Neblina no vale</p>')
        cls.post.categories.add(cls.category)

    # ---------- Posts ----------

    def test_listagem_tem_link_para_o_post(self):
        resposta = self.client.get(reverse('blog:post_list'))
        self.assertContains(resposta, 'Serra ao amanhecer')
        self.assertContains(resposta, reverse('blog:post_detail', args=[self.post.pk]))

    def test_detalhe_renderiza_html_e_categorias(self):
        resposta = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertContains(resposta, '<p>Neblina no vale</p>', html=True)
        self.assertContains(resposta, reverse('blog:category_detail', args=[self.category.pk]))

    def test_detalhe_de_post_inexistente_da_404(self):
        resposta = self.client.get(reverse('blog:post_detail', args=[99999]))
        self.assertEqual(resposta.status_code, 404)

    def test_criar_editar_e_remover_post(self):
        resposta = self.client.post(reverse('blog:post_create'), {
            'title': 'Post novo', 'content': '<p>texto</p>', 'categories': [self.category.pk],
        })
        novo = Post.objects.get(title='Post novo')
        self.assertRedirects(resposta, reverse('blog:post_detail', args=[novo.pk]))
        self.assertEqual(list(novo.categories.all()), [self.category])

        self.client.post(reverse('blog:post_update', args=[novo.pk]), {
            'title': 'Post editado', 'content': '<p>outro texto</p>',
        })
        novo.refresh_from_db()
        self.assertEqual(novo.title, 'Post editado')

        confirmacao = self.client.get(reverse('blog:post_delete', args=[novo.pk]))
        self.assertContains(confirmacao, 'Sim, remover')
        resposta = self.client.post(reverse('blog:post_delete', args=[novo.pk]))
        self.assertRedirects(resposta, reverse('blog:post_list'))
        self.assertFalse(Post.objects.filter(pk=novo.pk).exists())

    def test_post_sem_titulo_nao_e_criado(self):
        resposta = self.client.post(reverse('blog:post_create'), {'title': '', 'content': '<p>x</p>'})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)

    # ---------- Comentários ----------

    def test_comentarios_do_mais_recente_para_o_mais_antigo(self):
        agora = timezone.now()
        Comment.objects.create(post=self.post, author=self.user, text='comentario-antigo-123',
                               pub_date=agora - timedelta(days=2))
        Comment.objects.create(post=self.post, author=self.user, text='comentario-recente-456',
                               pub_date=agora)
        html = self.client.get(reverse('blog:post_detail', args=[self.post.pk])).content.decode()
        self.assertLess(html.index('comentario-recente-456'), html.index('comentario-antigo-123'))

    def test_criar_comentario(self):
        url = reverse('blog:comment_create', args=[self.post.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        resposta = self.client.post(url, {'author': self.user.pk, 'text': 'Belo registro!'})
        self.assertRedirects(
            resposta, reverse('blog:post_detail', args=[self.post.pk]) + '#comentarios',
            fetch_redirect_response=False,
        )
        comentario = Comment.objects.get()
        self.assertEqual((comentario.post, comentario.author), (self.post, self.user))

    def test_comentar_em_post_inexistente_da_404(self):
        resposta = self.client.get(reverse('blog:comment_create', args=[99999]))
        self.assertEqual(resposta.status_code, 404)

    # ---------- Categorias ----------

    def test_listagem_de_categorias(self):
        resposta = self.client.get(reverse('blog:category_list'))
        self.assertContains(resposta, 'Paisagens')
        self.assertContains(resposta, reverse('blog:category_detail', args=[self.category.pk]))

    def test_pagina_de_categoria_reaproveita_listagem_de_posts(self):
        resposta = self.client.get(reverse('blog:category_detail', args=[self.category.pk]))
        self.assertTemplateUsed(resposta, 'blog/post_list.html')
        self.assertContains(resposta, 'Paisagens')
        self.assertContains(resposta, 'Serra ao amanhecer')

    def test_categoria_inexistente_da_404(self):
        resposta = self.client.get(reverse('blog:category_detail', args=[99999]))
        self.assertEqual(resposta.status_code, 404)


class PopularBancoTests(TestCase):
    def test_comando_cria_os_dados_minimos_da_parte_4(self):
        call_command('popular_banco', stdout=StringIO())
        self.assertGreaterEqual(Post.objects.count(), 3)
        self.assertGreaterEqual(Category.objects.count(), 3)
        sem_comentario = [p for p in Post.objects.all() if p.comments.count() == 0]
        self.assertEqual(len(sem_comentario), 1)
        for post in Post.objects.all():
            self.assertGreaterEqual(post.categories.count(), 1)
            if post.comments.exists():
                self.assertIn(post.comments.count(), (2, 3))
        varias = [p for p in Post.objects.all() if p.categories.count() > 1]
        self.assertGreaterEqual(len(varias), 2)

    def test_comando_pode_rodar_duas_vezes(self):
        call_command('popular_banco', stdout=StringIO())
        call_command('popular_banco', stdout=StringIO())
        self.assertEqual(Post.objects.count(), 4)
