from django.contrib import admin
from .models import Category, Post, Comment, Vote

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('order', 'name')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'type', 'is_pinned', 'created_at', 'views_count')
    list_filter = ('type', 'is_pinned', 'is_locked', 'category')
    search_fields = ('title', 'content', 'author__username')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    list_editable = ('is_pinned',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'is_edited')
    list_filter = ('is_edited', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    raw_id_fields = ('author', 'post', 'parent')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('user__username', 'post__title')
    raw_id_fields = ('user', 'post')
