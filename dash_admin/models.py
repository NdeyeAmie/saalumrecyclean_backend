from django.db import models


# ── Modèle Événement ──────────────────────────────────────────────────────────

class Article(models.Model):
    titre       = models.CharField(max_length=255)
    description = models.TextField()
    date_event  = models.DateField(verbose_name="Date de l'événement")
    image       = models.ImageField(upload_to='articles/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering         = ['-date_event']
        verbose_name     = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.titre


# ── Modèle Blog ───────────────────────────────────────────────────────────────

class BlogPost(models.Model):

    CATEGORY_CHOICES = [
        ('sensibilisation', 'Sensibilisation'),
        ('partenariats',    'Partenariats'),
        ('actions_terrain', 'Actions terrain'),
        ('formation',       'Formation'),
        ('reseau',          'Réseau'),
        ('evenements',      'Événements'),
        ('decouverte',      'Découverte'),
    ]

    TAG_CHOICES = [
        ('a_la_une',      'À la une'),
        ('international', 'International'),
        ('terrain',       'Terrain'),
        ('reportage',     'Reportage'),
        ('evenement',     'Événement'),
        ('reseau',        'Réseau'),
        ('formation',     'Formation'),
    ]

    titre      = models.CharField(max_length=255, verbose_name="Titre")
    excerpt    = models.CharField(max_length=400, verbose_name="Accroche (court résumé)")
    contenu    = models.TextField(verbose_name="Contenu complet de l'article")
    categorie  = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Catégorie")
    tag        = models.CharField(max_length=50, choices=TAG_CHOICES, default='terrain', verbose_name="Tag affiché")
    read_time  = models.PositiveSmallIntegerField(default=3, verbose_name="Temps de lecture (minutes)")
    date_pub   = models.DateField(verbose_name="Date de publication")
    image      = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Image")
    en_vedette = models.BooleanField(default=False, verbose_name="Article vedette (à la une)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering         = ['-date_pub']
        verbose_name     = "Article de blog"
        verbose_name_plural = "Articles de blog"

    def __str__(self):
        return self.titre

    @property
    def categorie_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.categorie, self.categorie)

    @property
    def tag_display(self):
        return dict(self.TAG_CHOICES).get(self.tag, self.tag)

    @property
    def date_formatee(self):
        mois_fr = {
            1: 'JANVIER',   2: 'FÉVRIER',  3: 'MARS',      4: 'AVRIL',
            5: 'MAI',       6: 'JUIN',     7: 'JUILLET',   8: 'AOÛT',
            9: 'SEPTEMBRE', 10: 'OCTOBRE', 11: 'NOVEMBRE', 12: 'DÉCEMBRE',
        }
        return f"{self.date_pub.day:02d} {mois_fr[self.date_pub.month]} {self.date_pub.year}"