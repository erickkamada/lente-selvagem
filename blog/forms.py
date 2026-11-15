from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ex.: Amanhecer na Serra da Mantiqueira'}),
            'content': forms.Textarea(attrs={'rows': 16}),
        }
