"""
Views do blog: CRUD de posts com classes genéricas e criação de comentários.
"""
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm
from .models import Comment, Post


class PostListView(ListView):
    """Lista os posts (template blog/post_list.html, variável post_list)."""
    model = Post


class PostDetailView(DetailView):
    """Exibe um post com seus comentários. Responde com 404 se o post não existir."""
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
