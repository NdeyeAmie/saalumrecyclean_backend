from django import forms
from .models import Article


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