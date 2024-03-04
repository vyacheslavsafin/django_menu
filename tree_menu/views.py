from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from tree_menu.models import Menu


class IndexView(TemplateView):
    template_name = "tree_menu/index.html"
