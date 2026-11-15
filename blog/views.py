"""
Versão 2 das views: apenas views funcionais, utilizando um Django form
(PostForm) para validar os dados.
"""
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def post_list(request):
    """Lista os títulos dos posts, do mais recente para o mais antigo."""
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'post_list': posts})


def post_detail(request, pk):
    """Exibe um post. Responde com 404 se o post não existir."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_create(request):
    """Cria um post. Se o formulário for inválido, ele é exibido com os erros."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


def post_update(request, pk):
    """Edita um post existente usando o mesmo formulário da criação."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})


def post_delete(request, pk):
    """Mostra a página de confirmação (GET) e remove o post (POST)."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
