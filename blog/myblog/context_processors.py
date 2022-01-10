from .models import Photo

def image_featured(request):
    return {'image_featured': Photo.objects.filter(feature_image=True), }
