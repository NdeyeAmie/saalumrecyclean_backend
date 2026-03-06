from django import forms
from .models import Article, BlogPost


# ── Formulaire Événement ──────────────────────────────────────────────────────

class ArticleForm(forms.ModelForm):
    class Meta:
        model  = Article
        fields = ['titre', 'date_event', 'description', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Titre de l'article ou événement",
            }),
            'date_event': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': "Description complète de l'événement...",
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'titre':       'Titre',
            'date_event':  "Date de l'événement",
            'description': 'Description',
            'image':       'Image',
        }


# ── Formulaire Blog ───────────────────────────────────────────────────────────

class BlogPostForm(forms.ModelForm):
    class Meta:
        model  = BlogPost
        fields = [
            'titre', 'excerpt', 'contenu',
            'categorie', 'tag', 'read_time',
            'date_pub', 'image', 'en_vedette',
        ]
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Titre de l'article",
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Courte accroche affichée sur la carte (max 400 caractères)...",
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': "Contenu complet de l'article. Séparez les paragraphes par une ligne vide.",
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-select',
            }),
            'tag': forms.Select(attrs={
                'class': 'form-select',
            }),
            'read_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 60,
            }),
            'date_pub': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'en_vedette': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'titre':      'Titre',
            'excerpt':    'Accroche',
            'contenu':    'Contenu',
            'categorie':  'Catégorie',
            'tag':        'Tag',
            'read_time':  'Temps de lecture (min)',
            'date_pub':   'Date de publication',
            'image':      'Image de couverture',
            'en_vedette': 'Mettre en vedette (à la une)',
        }