from django.urls import path
from rest_framework.routers import SimpleRouter

from graph_recsys.apps import GraphRecsysConfig
from graph_recsys.views import PreferCreateView, PreferUpdateView, MainPageView

app_name = GraphRecsysConfig.name



urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('prefer/create', PreferCreateView.as_view(), name='create'),
    path('prefer/update/<int:pk>', PreferUpdateView.as_view(), name='update'),
]