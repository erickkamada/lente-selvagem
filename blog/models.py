from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField('título', max_length=200)
    # O conteúdo é guardado como HTML e exibido no template com o filtro safe
    content = models.TextField(
        'conteúdo (HTML)',
        help_text='Aceita HTML, por exemplo as tags p, h3, figure e img.',
    )
    pub_date = models.DateTimeField('data de postagem', default=timezone.now)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
