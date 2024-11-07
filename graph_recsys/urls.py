from tkinter.font import names

from graph_recsys.apps import GraphRecsysConfig
from graph_recsys.views import set_prefers
from django.urls import path

app_name = GraphRecsysConfig.name

urlpatterns = [
    path('prefers', set_prefers.as_view(), name='set_prefers'),
]