from django.contrib import admin
from .models import Post, Author, Comment, Photo









@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'publish', 'status', 'featured', 'comments_option')
    list_filter = ('author', 'publish', 'featured', 'status')
    search_fields = ('title', 'summary', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

@admin.register(Photo)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin_thumbnail', 'lens', 'caption', 'file_size', 'description')
    #exclude = ['posts']




