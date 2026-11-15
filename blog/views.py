"""
Versão 3 das views: classes genéricas ListView, DetailView, CreateView,
UpdateView e DeleteView.
"""
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    """Lista os posts (template blog/post_list.html, variável post_list)."""
    model = Post


class PostDetailView(DetailView):
    """Exibe um post. A DetailView já responde com 404 se o post não existir."""
    model = Post


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
