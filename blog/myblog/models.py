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
from blog.settings import MEDIA_ROOT
from os.path import join as pjoin
from sorl.thumbnail import ImageField





# TODO right click diasbled in js.html
# TODO add save to action menu in admin
# TODO put managers in seperate manager file
# TODO its curently saveing featuired images seperatly so need to write function to gen thumnail


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class FeaturedManager(models.Manager):
    def get_queryset(self):
        return super(FeaturedManager, self).get_queryset().filter(featured=True, status='published')


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

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edited = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default='unpublished')
    featured = models.BooleanField(default=False)
    comments_option = models.BooleanField(default=True)
    objects = models.Manager()
    published = PublishedManager()
    feature = FeaturedManager()
    tags = TaggableManager(verbose_name="Add Tags", help_text="Use comma to separate")


    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title



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


class Album(models.Model):
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    @mark_safe
    def images(self):
        lst = [x.image.name for x in self.photos.all()]
        lst = ["<a href='/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
        return ",".join(lst)

    images.allow_tags = True



class Photo(models.Model):
    image = models.ImageField(upload_to='images')
    title = models.CharField(max_length=100)
    albums = models.ManyToManyField(Album, blank=True, related_name='photos')
    feature_image = models.BooleanField(default=False)
    description = models.CharField(editable=False, max_length=150, blank=True)
    posts = models.ManyToManyField(Post, blank=True, related_name='pictures')

    lens = models.TextField(editable=False, max_length=100, default='Lens Data')
    caption = models.CharField(editable=False, max_length=1000, default='Caption info')
    file_size = models.CharField(editable=False, max_length=20, default='File_size')
    width = models.IntegerField(blank=True, null=True, editable=False)
    height = models.IntegerField(blank=True, null=True, editable=False)
    categories = models.ForeignKey(Catagory, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager
    info = models.TextField(default='**info empty**', blank=True, help_text="editable caption info no reversable")
    exif = ExifField(source='image', denormalized_fields={'lens': exifgetter('LensID'),
                                                          'caption': exifgetter('Description'),
                                                          'file_size': exifgetter('FileSize'),
                                                          'description': exifgetter('Headline')

                                                          })


    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        """Get EXIF"""
        im = Image.open(self.image.path)
        try:
            info = im.getexif()[0x010e]
            self.info = info
        except KeyError:
            pass
        """Save image dimensions."""
        im = Image.open(pjoin(MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size
        im.save(self.image.path)
        super(Photo, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return ",".join(lst)

    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)















