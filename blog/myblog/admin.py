from django.contrib import admin
from .models import Post, Author, Comment, Photo, Catagory
from django.utils.safestring import mark_safe
from django import forms


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','author_thumbnail',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'publish', 'status', 'featured', 'comments_option', 'show_pictures')
    list_filter = ('author', 'publish', 'featured', 'status')
    search_fields = ('title', 'summary', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    @mark_safe
    def show_pictures(self, obj):
       images = ''
       for item in obj.pictures.all():
           images += '<img src="%s" height="50" width="50"/>' % item.image.url
       return images

    show_pictures.allow_tags = True



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


class PostForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['info']
        filter_horizontal = ['Posts']
        fields = '__all__'

@admin.register(Photo)
class ImageAdmin(admin.ModelAdmin):
    list_display  = ('title', 'info', 'feature_image', 'admin_thumbnail', 'lens', 'caption', 'file_size', 'description', 'get_category',)
    list_editable = ('info',)
    search_fields = ('title', 'caption', 'description')
    form = PostForm


    # This provides access to FK Category model
    @admin.display(description='Category', ordering='categories__name')
    def get_category(self, obj):
        return obj.categories

    @mark_safe
    def admin_thumbnail(self, obj):
        return u'<img src="%s" height="100px" />' % (obj.image.url)

    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True



@admin.register(Catagory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}



