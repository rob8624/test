from django.contrib import admin
from .models import Post, Author, Comment, Photo


# TODO Try to add an in-line representation on Photo model in Admin/Post so I can upload pics directly to posts

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

# TODO check get_photo method.....it is designed to add thumbnails of photo related to a Post but need coding
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'publish', 'status', 'featured', 'comments_option', 'get_photo')
    list_filter = ('author', 'publish', 'featured', 'status')
    search_fields = ('title', 'summary', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def get_photo(self, obj):
        return obj.pictures.all()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

@admin.register(Photo)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin_thumbnail', 'lens', 'caption', 'file_size', 'description')
    #exclude = ['posts']




