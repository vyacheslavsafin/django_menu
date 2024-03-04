from django.urls import path

from tree_menu.apps import TreeMenuConfig
from tree_menu.views import IndexView

app_name = TreeMenuConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
