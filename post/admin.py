from django import forms
from django.contrib import admin
from .models import Post, Like, Bookmark, Comment, Tag


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = '__all__'

class LikeInline(admin.TabularInline):
    model = Like

class CommentInline(admin.TabularInline):
    model = Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'nickname', 'content', 'created_at']
    list_display_links = ['author', 'nickname', 'content']
    form = PostForm
    inlines = [LikeInline, CommentInline]

    def nickname(request, post):
        return post.author.profile.nickname

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    # click 했을 때 링크가 생기는 부분
    list_display_links = ['post', 'user']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    # click 했을 때 링크가 생기는 부분
    list_display_links = ['post', 'user']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'content', 'author', 'created_at']
    list_display_links = ['post', 'content']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
