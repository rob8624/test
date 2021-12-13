from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'post/detail.html',
                  {'post': post})

class PostFeaturedView(ListView):
    queryset = Post.feature.all()
    context_object_name = 'featured'
    paginate_by = 3
    template_name = 'post/featured.html'
    #featured = Post.feature.all()
    #return render(request, 'post/featured.html',
                  #{'featured': featured},)


