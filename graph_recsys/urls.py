from django.urls import path
from rest_framework.routers import SimpleRouter

from graph_recsys.apps import GraphRecsysConfig
from graph_recsys.views import PreferCreateView, PreferUpdateView, MainPageView, TrackUpdateView, add_listener, \
    add_genre_to_prefer, clear_play_list, StatisticsPageView

app_name = GraphRecsysConfig.name



urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('statistics/', StatisticsPageView.as_view(), name='statistics'),
    path('prefer/create', PreferCreateView.as_view(), name='create'),
    path('prefer/update/<int:pk>/', PreferUpdateView.as_view(), name='update'),
    path('track/update/<int:pk>/', add_listener, name='add_listener'),
    path('track/genre_check/<int:pk>/', add_genre_to_prefer, name='check_genre'),
    path('track/clear/', clear_play_list, name='clear'),
]