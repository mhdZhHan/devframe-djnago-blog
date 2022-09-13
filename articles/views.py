from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from articles.models import Article
from articles.forms import LoginForm, RegisterForm, ArticleForm, ArticleUpdateForm


def articles(request):
    # return HttpResponse('Hello world')
    articles = Article.objects.all().order_by('-published')
    # pagination
    paginator = Paginator(articles, 4)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        "articles": articles,
        "page": page,
    }
    return render(request, 'articles.html', context=context)


def article_details(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {"article": article}
    return render(request, 'details.html', context=context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Successfully logged')
            else:
                return HttpResponse("Invalid username or password")
    else:
        form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, 'auth/login.html', context)


def create_user(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False) # commit=False => that means donot want to commit the new user data to db
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {
                'user': new_user,
            }
            return render(request, 'auth/register_done.html', context)
    else:
        user_form = RegisterForm()
    context = {
        'form': user_form,
    }
    return render(request, 'auth/register.html', context)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('/articles')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'add_article.html', context)


@login_required
def update_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = ArticleUpdateForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('/articles')
    context = {
        'form': form,
    }
    return render(request, 'update_article.html', context)


@login_required
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.delete()
    return render(request, 'article_deleted.html')

