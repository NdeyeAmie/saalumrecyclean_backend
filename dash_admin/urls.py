from django.urls import path
from . import views

app_name = 'dash_admin'

urlpatterns = [

    # ── Auth ──────────────────────────────────────────────────────────────────
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── Dashboard ─────────────────────────────────────────────────────────────
    path('', views.dashboard, name='dashboard'),

    # ── Articles (Événements) ─────────────────────────────────────────────────
    path('articles/ajout/',               views.ajout_article,     name='ajout_article'),
    path('articles/liste/',               views.liste_articles,    name='liste_articles'),
    path('articles/voir/<int:pk>/',       views.voir_article,      name='voir_article'),
    path('articles/modifier/<int:pk>/',   views.modifier_article,  name='modifier_article'),
    path('articles/supprimer/<int:pk>/',  views.supprimer_article, name='supprimer_article'),

    # ── Blog ──────────────────────────────────────────────────────────────────
    path('blog/ajout/',               views.ajout_blog,     name='ajout_blog'),
    path('blog/liste/',               views.liste_blog,     name='liste_blog'),
    path('blog/voir/<int:pk>/',       views.voir_blog,      name='voir_blog'),
    path('blog/modifier/<int:pk>/',   views.modifier_blog,  name='modifier_blog'),
    path('blog/supprimer/<int:pk>/',  views.supprimer_blog, name='supprimer_blog'),

    # ── API JSON (consommées par React) ───────────────────────────────────────
    path('api/articles/',          views.api_articles,    name='api_articles'),
    path('api/blog/',              views.api_blog,        name='api_blog'),
    path('api/blog/<int:pk>/',     views.api_blog_detail, name='api_blog_detail'),
]