"""
Versão 1 das views: apenas views funcionais, sem Django forms
e sem validação de dados.
"""
from django.shortcuts import get_object_or_404, redirect, render

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
    """Cria um post a partir dos dados enviados pelo formulário HTML."""
    if request.method == 'POST':
        post = Post.objects.create(
            title=request.POST.get('title', ''),
            content=request.POST.get('content', ''),
        )
        return redirect('blog:post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html')


def post_update(request, pk):
    """Edita um post existente."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title', '')
        post.content = request.POST.get('content', '')
        post.save()
        return redirect('blog:post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'post': post})


def post_delete(request, pk):
    """Mostra a página de confirmação (GET) e remove o post (POST)."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
