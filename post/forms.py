from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    # 중복 값을 받지 않기 위해 required=False
    photo = forms.ImageField(label='', required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'post-new-content',
        'rows': 5,
        'cols': 50,
        'placeholder': '140자 까지 등록 가능합니다.'
    }))

    class Meta:
        model = Post
        fields = ['photo', 'content']

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'comment-form',
        'size': '70px',
        'placeholder': '댓글 달기...',
        'maxlength': 40,
    }))

    class Meta:
        model = Comment
        fields = ['content']
