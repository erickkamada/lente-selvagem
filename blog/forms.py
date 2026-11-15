from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ex.: Amanhecer na Serra da Mantiqueira'}),
            'content': forms.Textarea(attrs={'rows': 16}),
            'categories': forms.CheckboxSelectMultiple,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        labels = {'author': 'Autor(a)', 'text': 'Comentário'}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O que você achou desta foto?'}),
        }
