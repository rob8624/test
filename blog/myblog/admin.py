from django.contrib import admin
from .models import Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'image_tag', 'slug', 'publish', 'status', 'featured')
    list_filter = ('author', 'publish', 'status')
    search_fields = ('title', 'summary', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')





# Register your models here.
