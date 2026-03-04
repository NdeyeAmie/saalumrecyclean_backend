from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms  import ArticleForm
from django.http import JsonResponse


# ── API JSON pour React ───────────────────────────────────────────────────────


def api_articles(request):
    articles = Article.objects.all()
    data = []
    for article in articles:
        data.append({
            'id': article.id,
            'titre': article.titre,
            'description': article.description,
            'date_event': article.date_event.strftime('%d %B').upper(),
            'image': request.build_absolute_uri(article.image.url) if article.image else None,
        })
    return JsonResponse(data, safe=False)
# ── Auth ──────────────────────────────────────────────────────────────────────

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


# ── Dashboard ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    articles = Article.objects.all()
    context  = {'articles': articles, 'total': articles.count()}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/dashboard_partial.html', context)
    return render(request, 'index.html', context)


# ── Article : Ajout ───────────────────────────────────────────────────────────

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


# ── Article : Liste ───────────────────────────────────────────────────────────

@login_required
def liste_articles(request):
    articles = Article.objects.all()
    context  = {'articles': articles}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/liste_articles_partial.html', context)
    return render(request, 'pages/liste_articles.html', context)


# ── Article : Voir détail ─────────────────────────────────────────────────────

@login_required
def voir_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    if request.headers.get('HX-Request'):
        return render(request, 'pages/voir_article_partial.html', context)
    return render(request, 'pages/voir_article.html', context)


# ── Article : Modifier ────────────────────────────────────────────────────────

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


# ── Article : Supprimer ───────────────────────────────────────────────────────

@login_required
def supprimer_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        # Supprimer aussi le fichier image du disque
        if article.image:
            import os
            if os.path.isfile(article.image.path):
                os.remove(article.image.path)
        article.delete()
        # Retourner la liste mise à jour via HTMX
        articles = Article.objects.all()
        if request.headers.get('HX-Request'):
            return render(request, 'pages/liste_articles_partial.html', {'articles': articles})
        return redirect('dash_admin:liste_articles')
    return redirect('dash_admin:liste_articles')