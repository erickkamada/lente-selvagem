"""
Views do blog: CRUD de posts com classes genéricas, criação de comentários
e páginas de categorias.
"""
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


# ---------- Posts ----------

class PostListView(ListView):
    """Lista os posts (template blog/post_list.html, variável post_list)."""
    queryset = Post.objects.prefetch_related('categories')


class PostDetailView(DetailView):
    """Exibe um post com categorias e comentários. 404 se o post não existir."""
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Comentários do mais recente para o mais antigo
        context['comments'] = self.object.comments.select_related('author').order_by('-pub_date')
        # Formulário para comentar direto da página do post
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(CreateView):
    """Cria um post e redireciona para Post.get_absolute_url()."""
    model = Post
    form_class = PostForm


class PostUpdateView(UpdateView):
    """Edita um post (mesmo template da criação: blog/post_form.html)."""
    model = Post
    form_class = PostForm


class PostDeleteView(DeleteView):
    """GET mostra blog/post_confirm_delete.html; POST remove o post."""
    model = Post
    success_url = reverse_lazy('blog:post_list')


# ---------- Comentários ----------

class CommentCreateView(CreateView):
    """Cria um comentário no post indicado pela URL (template blog/comment_form.html)."""
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        # Busca o post antes de tudo: 404 se ele não existir
        self.blog_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.blog_post
        return context

    def form_valid(self, form):
        # O post não vem do formulário: é o da URL
        form.instance.post = self.blog_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.blog_post.pk}) + '#comentarios'


# ---------- Categorias ----------

class CategoryListView(ListView):
    """Lista as categorias com a quantidade de posts de cada uma."""
    queryset = Category.objects.annotate(num_posts=Count('posts'))


class CategoryDetailView(DetailView):
    """
    Página individual de categoria. Reaproveita o template de listagem de
    posts da parte 1, que exibe o nome da categoria quando ela está no contexto.
    A DetailView responde com 404 se a categoria não existir.
    """
    model = Category
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = self.object.posts.prefetch_related('categories')
        return context
