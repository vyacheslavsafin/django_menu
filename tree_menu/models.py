from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название меню')
    slug = models.SlugField(max_length=100, verbose_name="slug")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class MenuItem(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название пункта меню')
    slug = models.SlugField(max_length=100, verbose_name="slug")
    menu = models.ForeignKey(Menu, blank=True, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='childrens', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
