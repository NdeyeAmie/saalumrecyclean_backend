from django.db import models


class Article(models.Model):
    titre       = models.CharField(max_length=255)
    description = models.TextField()
    date_event  = models.DateField(verbose_name="Date de l'événement")
    image       = models.ImageField(upload_to='articles/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_event']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.titre