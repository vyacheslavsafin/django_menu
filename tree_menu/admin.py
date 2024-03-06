from django.contrib import admin

from tree_menu.models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'parent')
    list_filter = ('menu',)
    search_fields = ('title', 'slug')
    ordering = ('pk',)
