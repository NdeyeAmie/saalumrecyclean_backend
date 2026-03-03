from django.urls import path
from . import views

app_name = 'dash_admin'

urlpatterns = [
    path('',                             views.dashboard,         name='dashboard'),
    path('articles/ajout/',              views.ajout_article,     name='ajout_article'),
    path('articles/liste/',              views.liste_articles,    name='liste_articles'),
    path('articles/voir/<int:pk>/',      views.voir_article,      name='voir_article'),
    path('articles/modifier/<int:pk>/',  views.modifier_article,  name='modifier_article'),
    path('articles/supprimer/<int:pk>/', views.supprimer_article, name='supprimer_article'),
    path('login/',                       views.login_view,        name='login'),
    path('logout/',                      views.logout_view,       name='logout'),
]