from django.urls import path
from . import views
from django.views.generic.dates import ArchiveIndexView
from .models import Post

app_name = 'myblog'

urlpatterns = [

    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('<slug:gallery>/<int:pk>', views.gallery_detail, name='gallery_detail'),
    path('contact/', views.contact_form, name='contact_form'),
    path('archive/',
         ArchiveIndexView.as_view(model=Post, date_field="created"),
         name="post_archive"),
    path('purchase/', views.purchase_page, name='purchase'),



    ]
