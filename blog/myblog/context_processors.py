from .models import Photo, Post

def image_featured(request):
    return {'image_featured': Photo.objects.filter(feature_image=True), }


def posts_all(request):
    return {'posts_all' : Post.published.order_by('publish'), }