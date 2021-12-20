from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse

#add cutoms model managers so we can use for example Post.published.all() instead of post.objects.all()
#also added a model manager to only show posts marked High importance, which can ber used to show certain post as
#featured

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class FeaturedManager(models.Manager):
    def get_queryset(self):
        return super(FeaturedManager, self).get_queryset().filter(featured=True, status='published')




#define author model

class Author(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=70,blank=True,unique=True)
    bio = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

#define Post model

class Post(models.Model):
    STATUS = (
        ('published', 'Published'),
        ('unpublished', 'Unpublished'),
    )

    title = models.CharField(max_length=250, null=False, blank=False)
    summary = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique_for_date='publish')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_posts')
    # CASCADE means when a user is deleted so are all their blog posts
    body = models.CharField(max_length=5000, null=False, blank=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default='unpublished')
    featured = models.BooleanField(default=False)
    #model managers
    objects = models.Manager()
    published = PublishedManager()
    feature = FeaturedManager()

    #Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table),
    # or human-readable singular and plural names (verbose_name and verbose_name_plural).
    # None are required, and adding class Meta to a model is completely optional.

    class Meta:
        ordering = ('-publish',)

    # returs a strinf of the class(what appears in admin page to represent model
    def __str__(self):
        return self.title

    # method to return the canonical URL for the model
    def get_absolute_url(self):
        return reverse('myblog:post_detail', args=[self.publish.year,
                                                   self.publish.month,
                                                   self.publish.day,
                                                   self.slug])


#commenting modle

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

