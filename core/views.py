from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import UserRegisterForm
from .models import Post, Comment

def index(request):
    posts = Post.objects.all()[:5]
    context = {
        'posts':posts
    }
    return render(request, 'index.html', context)


def blog(request):
    posts = Post.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 4)

    try:
        obj = paginator.page(page)
    except PageNotAnInteger: 
        obj = paginator.page(1)
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)

    context = {
        'posts':obj
    }
    return render(request, 'blog.html', context)

def detailedView(request, slug):
    posts = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=posts)
    commentCount = Comment.objects.filter(post=posts).count()
    context = {
        'posts':posts,
        'comments':comments,
        'commentCount':commentCount
    }
    return render(request, 'detailView.html', context)


def search(request):
    if request.method == 'POST':
        search = request.POST['searched']
        posts = Post.objects.filter(title__contains=search)
        return render(request, 'blog.html', {'posts':posts})
    else:
        posts = Post.objects.all()
        return render(request, 'blog.html',{'posts':posts})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(request,username=username, password=password)

        if user is not None:
            form = login(request,user)
            return redirect('/')
        return render(request, 'auth/login.html', {'error':'Invalid Username/Password'})
    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                return redirect('/')
        return render(request, 'auth/signup.html', {'form': form})
    return render(request, 'auth/signup.html')


def comment(request):
    if request.method == 'POST':
        print('called')
    return render(request, 'detailView.html')