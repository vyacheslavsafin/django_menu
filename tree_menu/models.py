from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название меню')
    slug = models.SlugField(max_length=100, verbose_name="slug")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
