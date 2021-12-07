from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


#define Post model

class Post(models.Model):
    STATUS = (
        ('published', 'Published'),
        ('unpublished', 'Unpublished'),
    )

    IMPORTANCE = (
        ('high', 'High'),
        ('medium', 'medium'),
        ('low', 'Low'),
    )

    title = models.CharField(max_length=250, null=False, blank=False)
    summary = models.CharField(max_length=100)
    slug = models.SlugField(unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bog_posts')
    author_image = models.ImageField(upload_to='images/authors/', null=True, blank=True)
    # CASCADE means when a user is deleted so are all their blog posts
    body = models.CharField(max_length=5000, null=False, blank=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default='unpublished')
    importance = models.CharField(max_length=50, choices=IMPORTANCE, default='high')

    # function that returns author_image to admin site
    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="50" height="50" />' % (self.author_image))

    image_tag.allow_tags = True

    #Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table),
    # or human-readable singular and plural names (verbose_name and verbose_name_plural).
    # None are required, and adding class Meta to a model is completely optional.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title