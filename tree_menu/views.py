from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from tree_menu.models import Menu


class IndexView(TemplateView):
    template_name = "tree_menu/index.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.filter(slug='main_menu').first()
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = super().get(request, *args, **kwargs)
        print("Количество запросов к базе данных: ", len(connection.queries))
        return response
