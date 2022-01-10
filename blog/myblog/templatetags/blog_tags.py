from django import template
from ..models import Post, Photo
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('post/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts' : latest_posts}


@register.inclusion_tag('post/featured_posts.html')
def featured_posts(count=5):
    featured_posts = Post.feature.all()[:count]
    return {'featured_posts' : featured_posts }

@register.inclusion_tag('post/feature_image.html')
def featured_images():
    feature_images = Photo.objects.filter(feature_image=True)
    return {'feature_images' : featured_images }