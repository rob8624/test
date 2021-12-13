from django.urls import path
from . import views

app_name = 'myblog'

urlpatterns = [
    #post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    #path('featured/', views.post_featured, name='post_featured'),
    path('featured/', views.PostFeaturedView.as_view(), name='featured_list')
]
