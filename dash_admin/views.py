from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Article, BlogPost
from .forms  import ArticleForm, BlogPostForm
import os


# ══════════════════════════════════════════════════════════════════════════════
# API JSON  (consommées par React)
# ══════════════════════════════════════════════════════════════════════════════

def api_articles(request):
    articles = Article.objects.all()
    data = []
    for article in articles:
        image_url = None
        if article.image:
            image_url = request.build_absolute_uri(article.image.url)
            image_url = image_url.replace('http://', 'https://')
        data.append({
            'id':          article.id,
            'titre':       article.titre,
            'description': article.description,
            'date_event':  article.date_event.strftime('%d %B').upper(),
            'image':       image_url,
        })
    return JsonResponse(data, safe=False)


def api_blog(request):
    posts     = BlogPost.objects.all()
    categorie = request.GET.get('categorie')
    if categorie and categorie != 'tous':
        posts = posts.filter(categorie=categorie)
    data = []
    for post in posts:
        image_url = None
        if post.image:
            image_url = request.build_absolute_uri(post.image.url)
            image_url = image_url.replace('http://', 'https://')
        data.append({
            'id':         post.id,
            'titre':      post.titre,
            'excerpt':    post.excerpt,
            'contenu':    post.contenu,
            'categorie':  post.categorie_display,
            'tag':        post.tag_display,
            'readTime':   f"{post.read_time} min",
            'date':       post.date_formatee,
            'image':      image_url,
            'en_vedette': post.en_vedette,
        })
    return JsonResponse(data, safe=False)


def api_blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    image_url = None
    if post.image:
        image_url = request.build_absolute_uri(post.image.url)
        image_url = image_url.replace('http://', 'https://')
    data = {
        'id':         post.id,
        'titre':      post.titre,
        'excerpt':    post.excerpt,
        'contenu':    post.contenu,
        'categorie':  post.categorie_display,
        'tag':        post.tag_display,
        'readTime':   f"{post.read_time} min",
        'date':       post.date_formatee,
        'image':      image_url,
        'en_vedette': post.en_vedette,
    }
    return JsonResponse(data)


# ══════════════════════════════════════════════════════════════════════════════
# Auth
# ══════════════════════════════════════════════════════════════════════════════

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dash_admin:dashboard')
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect('dash_admin:dashboard')
        error = 'Identifiants incorrects. Réessayez.'
    return render(request, 'pages/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('dash_admin:login')


# ══════════════════════════════════════════════════════════════════════════════
# Dashboard
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def dashboard(request):
    articles   = Article.objects.all()
    blog_posts = BlogPost.objects.all()
    context    = {
        'articles':        articles,
        'total':           articles.count(),
        'blog_posts':      blog_posts,
        'total_blog':      blog_posts.count(),
    }
    if request.headers.get('HX-Request'):
        return render(request, 'pages/dashboard_partial.html', context)
    return render(request, 'index.html', context)


# ══════════════════════════════════════════════════════════════════════════════
# Articles (Événements)
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def ajout_article(request):
    form    = ArticleForm()
    message = None
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = 'success'
            form    = ArticleForm()
    context = {'form': form, 'message': message}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/ajout_article_partial.html', context)
    return render(request, 'pages/ajout_article.html', context)


@login_required
def liste_articles(request):
    articles = Article.objects.all()
    context  = {'articles': articles}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/liste_articles_partial.html', context)
    return render(request, 'pages/liste_articles.html', context)


@login_required
def voir_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/voir_article_partial.html', context)
    return render(request, 'pages/voir_article.html', context)


@login_required
def modifier_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form    = ArticleForm(instance=article)
    message = None
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            message = 'success'
    context = {'form': form, 'article': article, 'message': message}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/modifier_article_partial.html', context)
    return render(request, 'pages/modifier_article.html', context)


@login_required
def supprimer_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        if article.image and os.path.isfile(article.image.path):
            os.remove(article.image.path)
        article.delete()
        articles = Article.objects.all()
        if request.headers.get('HX-Request'):
            return render(request, 'pages/liste_articles_partial.html', {'articles': articles})
        return redirect('dash_admin:liste_articles')
    return redirect('dash_admin:liste_articles')


# ══════════════════════════════════════════════════════════════════════════════
# Blog
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def liste_blog(request):
    posts   = BlogPost.objects.all()
    context = {'posts': posts, 'total': posts.count()}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/liste_blog_partial.html', context)
    return render(request, 'pages/liste_blog.html', context)


@login_required
def ajout_blog(request):
    form    = BlogPostForm()
    message = None
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Après succès : rediriger vers la liste
            from django.http import HttpResponse
            if request.headers.get('HX-Request'):
                response = HttpResponse()
                response['HX-Redirect'] = '/dash_admin/blog/liste/'
                return response
            return redirect('dash_admin:liste_blog')
        # Formulaire invalide : rester sur la page avec les erreurs
        message = 'error'
    context = {'form': form, 'message': message}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/ajout_blog_partial.html', context)
    return render(request, 'pages/ajout_blog.html', context)


@login_required
def voir_blog(request, pk):
    post    = get_object_or_404(BlogPost, pk=pk)
    context = {'post': post}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/voir_blog_partial.html', context)
    return render(request, 'pages/voir_blog.html', context)


@login_required
def modifier_blog(request, pk):
    post    = get_object_or_404(BlogPost, pk=pk)
    form    = BlogPostForm(instance=post)
    message = None
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            from django.http import HttpResponse
            if request.headers.get('HX-Request'):
                response = HttpResponse()
                response['HX-Redirect'] = f'/dash_admin/blog/voir/{pk}/'
                return response
            return redirect('dash_admin:voir_blog', pk=pk)
        message = 'error'
    context = {'form': form, 'post': post, 'message': message}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/modifier_blog_partial.html', context)
    return render(request, 'pages/modifier_blog.html', context)


@login_required
def supprimer_blog(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        if post.image and os.path.isfile(post.image.path):
            os.remove(post.image.path)
        post.delete()
        posts = BlogPost.objects.all()
        if request.headers.get('HX-Request'):
            return render(request, 'pages/liste_blog_partial.html', {'posts': posts})
        return redirect('dash_admin:liste_blog')
    return redirect('dash_admin:liste_blog')