from django.urls import path
from . import views


app_name = 'myblog'

urlpatterns = [

    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('featured/', views.PostFeaturedView.as_view(), name='featured_list'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
    path('pictures/', views.photo_list, name='photo_list'),
    path('feature_image/', views.feature_image, name='feature_image')
]
