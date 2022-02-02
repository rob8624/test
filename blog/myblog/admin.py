from django.contrib import admin
from .models import Post, Author, Comment, Photo, Catagory, Album
from django import forms
from django.utils.safestring import mark_safe
import admin_thumbnails
from imagekit.admin import AdminThumbnail


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        readonly_fields = ('caption',)
        exclude = ['info',]
        fields = '__all__'

@admin.register(Photo)
@admin_thumbnails.thumbnail('image')
class ImageAdmin(admin.ModelAdmin):
    list_display  = ('title', 'info', 'image_thumbnail', 'feature_image', 'file_size', 'description',
                     'get_category', "albums_", 'size',)

    readonly_fields = ('caption', 'size')
    list_editable = ('info',)
    search_fields = ('title', 'caption', 'description')
    list_filter = ["albums",]
    form = PhotoForm



    # This provides access to FK Category model
    @admin.display(description='Category', ordering='categories__name')
    def get_category(self, obj):
        return obj.categories

    class PhotoAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'admin_thumbnail')
        admin_thumbnail = AdminThumbnail(image_field='thumbnail')



@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", 'images', 'created']
    prepopulated_fields = {'slug': ('title',)}




@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','author_thumbnail',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cover', 'slug', 'publish', 'status', 'featured', 'comments_option', 'show_pictures',)
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




@admin.register(Catagory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}






























