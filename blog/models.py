from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('nome', max_length=100, unique=True)
    description = models.TextField('descrição')

    class Meta:
        ordering = ['name']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'pk': self.pk})


class Post(models.Model):
    title = models.CharField('título', max_length=200)
    # O conteúdo é guardado como HTML e exibido no template com o filtro safe
    content = models.TextField(
        'conteúdo (HTML)',
        help_text='Aceita HTML, por exemplo as tags p, h3, figure e img.',
    )
    pub_date = models.DateTimeField('data de postagem', default=timezone.now)
    # Um post pode estar em várias categorias, e uma categoria reúne vários posts
    categories = models.ManyToManyField(
        Category, related_name='posts', blank=True, verbose_name='categorias',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', verbose_name='post',
    )
    # O autor referencia o modelo de usuário configurado no projeto (User do Django)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name='autor',
    )
    text = models.TextField('texto')
    pub_date = models.DateTimeField('data de postagem', default=timezone.now)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'comentário'
        verbose_name_plural = 'comentários'

    def __str__(self):
        return f'{self.author} em "{self.post}"'
