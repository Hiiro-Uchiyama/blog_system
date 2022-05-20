from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag, Comment
from .forms import PostAddForm, ContactForm, CmtForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from functools import reduce
from operator import and_
from django.contrib import messages

## Function to display details of a currently unused blog.
## Retrieve the data that is associated with the id base.
def detail(request, post_id): # In addition to this function, there is another detail function at the bottom which should be used.
    post = get_object_or_404(Post, id=post_id) # get_object_or_404 Does it exist or not?
    comments = Comment.objects.filter(post=post).order_by()
    tag = post.tag
    recent_post = Post.objects.all().filter(tag=tag)
    liked = False # The like is the data associated with the post and is not allowed to be empty.
    ## trying to determine if it's being liked or not.
    if post.like.filter(id=request.user.id).exists():
        liked = True
    return render(request, 'blog_app/detail.html', {'post': post, 'liked': liked, 'recent_post': recent_post})

## Judge the search words.
## q != '' and q is not
def is_valid_q(q):
    return q != '' and q is not None

## Function to display the blog top page
def index(request):
    posts = Post.objects.all().order_by('-created_at') # -created_at
    title_or_user = request.GET.get('title_or_user') # title_or_user
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    tag = request.GET.get('tag')
    page_obj = paginate_query(request, posts, settings.PAGE_PER_ITEM)
    recent_post = Post.objects.all().order_by('-created_at')[:10] # Retrieve the first 10 most recent posts.
    try:
       tags = Tag.objects.get(tag='回答') # Retrieve the tag with the answer.
    except:
        tags = 0
    if tags: # If there is a tag, the posts with that tag will be retrieved.
        question_answer = posts.filter(tag__tag=tags)
    else: # If there is none, assign None.
        question_answer = None
    if is_valid_q(title_or_user):
        posts = posts.filter(Q(title__icontains=title_or_user)
                             | Q(user__username__icontains=title_or_user)
                             ).distinct()
    if is_valid_q(date_min):
        posts = posts.filter(created_at__gte=date_min)
    if is_valid_q(date_max):
        posts = posts.filter(created_at__lt=date_max)
    if is_valid_q(tag) and tag != 'タグを選択...':
        posts = posts.filter(tag__tag=tag)
    return render(request, 'index.html',
                  {'posts': posts, 'title_or_user': title_or_user, 'date_min': date_min, 'date_max': date_max, 'tag': tag, 'page_obj': page_obj, 'recent_post': recent_post,'question_answer':question_answer})

## Function to display the top page of the blog
def blog(request):
    blog = Post.objects.order_by('-id')
    blog_obj = Post.objects.order_by('created_at')
    page_obj = paginate_query(request, blog, settings.PAGE_PER_ITEM)
    keyword = request.GET.get('keyword')
    tag = Tag.objects.all()
    if keyword: # This is search form process.
        exclusion_list = set([' ', ' '])
        q_list = ''
        for i in keyword: # Determine if there is a word-for-word match.
            if i in exclusion_list: # The keywords are broken down and differentiated into individual letters.
                pass
            else:
                q_list += i
        query = reduce(
                    and_, [Q(title__icontains=q) | Q(text__icontains=q) for q in q_list]
                )
        blog = blog.filter(query)
        messages.success(request, '「{}」の検索結果'.format(keyword))
        return render(request, 'blog.html', {'blog': blog,'page_obj': page_obj,'tag':tag,'blog_obj':blog_obj})
    return render(request, 'blog.html', {'page_obj': page_obj,'tag':tag,'blog_obj':blog_obj})

## Function to display the index page
class IndexView(generic.ListView):
    model = Post
    template_name = 'blog.html'

    ## It supports searches for retrieved keywords.
    def get_queryset(self):
        queryset = Post.objects.order_by('-id')
        keyword = self.request.GET.get('keyword')
        if keyword:
            exclusion = set([' ', '　'])
            q_list = ''
            for i in keyword:
                if i in exclusion:
                    pass
                else:
                    q_list += i
            query = reduce(
                        and_, [Q(title__icontains=q) | Q(text__icontains=q) for q in q_list]
                    ) # Decompose a word and implement a search for each case.
            queryset = queryset.filter(query) # Conduct a search.
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        return queryset # object.

## Function to display details about the site
def about(request):
    recent_post = Post.objects.all().order_by('-created_at')[:4]
    return render(request, 'about.html', {'recent_post':recent_post})

## Function to display content about a service
def service(request):
    recent_post = Post.objects.all().order_by('-created_at')[:4]
    return render(request, 'services.html', {'recent_post':recent_post})

## Function to display contents related to a menu
def menu(request):
    return render(request, 'menu.html')

## Function to display contents related to a movie
def movie(request):
    return render(request, 'movie.html')

## Function to display case.html
def case(request):
    return render(request, 'cases.html')

## Functions for your enquiry
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            myself = form.cleaned_data['myself']
            recipients = [settings.EMAIL_HOST_USER]
            if myself:
                recipients.append(email)
            try:
                send_mail(name, message, email, recipients)
            except BadHeaderError:
                return HttpResponse('無効なヘッダーが見つかりました。')
            return redirect('blog_app:done')
    else:
        form = ContactForm()
    return render(request, 'blog_app/contact.html', {'form': form})

## Functions to display done.html
def done(request):
    return render(request, 'blog_app/done.html')

## Function to display the blog's details page
def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    liked = False
    tag = post.tag
    new_post = Post.objects.order_by('-created_at')[:10] # Get new blog posts
    recent_post = Post.objects.all().filter(tag=tag) # Retrieve posts that have the same tag as the original post on the blog.
    tags = Tag.objects.all()
    if post.like.filter(id=request.user.id).exists():
        liked = True
    if request.method == "POST":
        form = CmtForm(request.POST or None)
        if form.is_valid():
            text = request.POST.get('text')
            comment = Comment.objects.create(
                post=post, user=request.user, text=text)
            comment.save()
    else:
        form = CmtForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'liked': liked
    }
    ## ajax communication.
    ## https://qiita.com/skokado/items/a25d64cafa3db791b283
    if request.is_ajax(): # https://remotestance.com/blog/99/
        html = render_to_string('blog_app/comment.html',
                                context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'blog_app/detail.html', {'post': post, 'form': form, 'comments': comments, 'liked': liked, 'recent_post': recent_post, 'new_post': new_post,'tags':tags})

## Function to delete comments on a blog post
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('blog_app:detail', post_id=comment.post.id)

## Function to generate pagination.
def paginate_query(request, queryset, count): # The arguments are the queryset and the number of querysets per page that you want to generate pagination.
    paginator = Paginator(queryset, count) # Create an instance
    page = request.GET.get('page') # page contains the page that is currently displayed on the site.
    try:
        page_obj = paginator.page(page) # Store page in page_obj
    except PageNotAnInteger:
        page_obj = paginator.page(1) # If page is not divisible, put 1 in page_obj.
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages) # In the case of an empty page, the sum of the pages is stored in page_obj.
    return page_obj

## Function to display an Google Adsense certificate
def ads(request):
    return render(request, 'blog_app/ads.txt')

## class when you were trying to create a monthly list.
class PostArchiveMixin:
    model = Post
    paginate_by = 10
    date_field = 'created_at'
    template_name = 'blog_app/post_list.html'
    allow_empty = True
    make_object_list = True

class PostArchiveIndex(PostArchiveMixin, generic.ArchiveIndexView):
    """トップページ、全記事一覧"""
    pass

class PostYearArchiveIndex(PostArchiveMixin, generic.YearArchiveView):
    """年別の記事"""
    pass

class PostMonthArchiveIndex(PostArchiveMixin, generic.MonthArchiveView):
    """月別の記事"""
    month_format = '%m'

class PostDetail(generic.DetailView):
    """記事の詳細"""
    model = Post

class PostList(generic.ListView):
    model = Post

class PostDetail(generic.DetailView):
    model = Post