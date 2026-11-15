from django.contrib import admin

from .models import Category, Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    list_filter = ('categories',)
    search_fields = ('title', 'content')
    date_hierarchy = 'pub_date'
    filter_horizontal = ('categories',)
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'pub_date')
    list_filter = ('author',)
    search_fields = ('text',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
