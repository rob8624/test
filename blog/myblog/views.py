from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment, Photo, Album, Author
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm, ContactForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.views.generic.dates import ArchiveIndexView
from django.contrib import messages













def contact_form(request):
    contact = Author.objects.get(name='Robert Melen')
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            send_mail(name, message, email, ['admin@blog.com'])
            messages.success(request, 'Your comment will be checked and then added, thankyou.')
            return HttpResponseRedirect(request.path_info)

    return render(request, 'post/contact_form.html', {'form': form,
                                                      'contact': contact})







#blog post views


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    # list of active comments for this post
    comments = post.comments.filter(active=True)
    paginator = Paginator(comments, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment object but dont save to database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            #save the comment to the database
            new_comment.save()
            messages.success(request, 'Your message has been sent, I will reply asap!.')
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'post/detail.html',
                  {'post': post,
                   'posts' : posts,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                   })


class PostFeaturedView(ListView):
    queryset = Post.feature.all()
    context_object_name = 'featured'
    paginate_by = 3
    template_name = 'post/featured.html'


#form views

def post_share(request, post_id):
    #retrieve posts by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #form fields pass validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                          f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else: #.....send email
        form = EmailPostForm()
    return render(request, 'post/share.html', {'post': post,
                                                'form': form,
                                                'sent': sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                SearchVector('body', weight='B')

            search_query = SearchQuery(query)
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),
                                              ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,
                  'post/search.html',
                  {'form' : form,
                   'query' : query,
                   'results' : results})



def gallery_list(request):
    gallery = Album.objects.filter(public=True)
    paginator = Paginator(gallery, 4)
    page = request.GET.get('page')
    try:
        galleries = paginator.page(page)
    except PageNotAnInteger:
        galleries = paginator.page(1)
    except EmptyPage:
        galleries = paginator.page(paginator.num_pages)

    return render(request, 'gallery/gallery_list.html', {

        'galleries': galleries,
        })


def gallery_detail(request, gallery, pk):
    gallery = get_object_or_404(Album, slug=gallery, pk=pk)
    images = gallery.photos.all()
    return render(request,  'gallery/gallery_detail.html', {
                  'gallery': gallery,
    'images': images})