from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse
from taggit.managers import TaggableManager
from exiffield.fields import ExifField
from exiffield.getters import exifgetter
from PIL import Image
from django_resized import ResizedImageField
from PIL.ExifTags import TAGS

#add cutoms model managers so we can use for example Post.published.all() instead of post.objects.all()
#also added a model manager to only show posts marked High importance, which can ber used to show certain post as
#featured

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class FeaturedManager(models.Manager):
    def get_queryset(self):
        return super(FeaturedManager, self).get_queryset().filter(featured=True, status='published')





# TODO possibly add category model


class Author(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=70,blank=True,unique=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    photo = ResizedImageField(size=[500, 400], upload_to='authors', default='author pic')

    def __str__(self):
        return self.name

    @mark_safe
    def author_thumbnail(self):
        return u'<img src="%s" height="65px" />' % (self.photo.url)

    author_thumbnail.short_description = 'Thumbnail'
    author_thumbnail.allow_tags = True


class Post(models.Model):
    STATUS = (
        ('published', 'Published'),
        ('unpublished', 'Unpublished'),
    )

    title = models.CharField(max_length=250, null=False, blank=False)
    summary = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique_for_date='publish')
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               related_name='blog_posts', null=True)
    # CASCADE means when a user is deleted so are all their blog posts
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edited = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default='unpublished')
    featured = models.BooleanField(default=False)
    comments_option = models.BooleanField(default=True)

    #model managers
    objects = models.Manager()
    published = PublishedManager()
    feature = FeaturedManager()
    tags = TaggableManager(verbose_name="Add Tags", help_text="Use comma to separate")
    #Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table),
    # or human-readable singular and plural names (verbose_name and verbose_name_plural).
    # None are required, and adding class Meta to a model is completely optional.

    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title

    def show_pictures(self, obj):
        return obj.pictures.all()

    # method to return the canonical URL for the model
    def get_absolute_url(self):
        return reverse('myblog:post_detail', args=[self.publish.year,
                                                   self.publish.month,
                                                   self.publish.day,
                                                   self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Catagory(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(null=True)
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Description')

    class Meta:
        verbose_name_plural = 'Catagory'

    def __str__(self):
        return str(self.name)


class Photo(models.Model):
    image = models.ImageField(upload_to='images')
    title = models.CharField(max_length=100)
    feature_image = models.BooleanField(default=False)
    description = models.CharField(editable=False, max_length=150, blank=True)
    posts = models.ManyToManyField(Post, blank=True, related_name='pictures')
    lens = models.TextField(editable=False, max_length=100, default='Lens Data')
    caption = models.CharField(editable=False, max_length=1000, default='Caption info')
    file_size = models.CharField(editable=False, max_length=20, default='File_size')
    categories = models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager
    info = models.TextField(default='**info empty**', help_text="editable caption info no reversable")
    exif = ExifField(source='image', denormalized_fields={'lens': exifgetter('LensID'),
                                                          'caption': exifgetter('Description'),
                                                          'file_size': exifgetter('FileSize'),
                                                          'description': exifgetter('Headline')

                                                          })

    def __str__(self):
        return self.title

    @mark_safe
    def admin_thumbnail(self):
        return u'<img src="%s" height="65px" />' % (self.image.url)
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True


    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        im = Image.open(self.image.path)
        try:
            info = im.getexif()[0x010e]
            self.info = info
        except KeyError:
            pass

            # for tag, value in info.items():
        #     decoded = TAGS.get(tag, tag)
        #     info[decoded] = value



        im.save(self.image.path)

        super(Photo, self).save(*args, **kwargs)




class IPTC(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    data = models.CharField(max_length=500, default='caption')

    # def caption(self):
    #     images = Photo.objects.all()
    #
    #     return images.info




    class Meta:
        verbose_name_plural = "IPTC"


    def __str__(self):
        return self.picture.title







