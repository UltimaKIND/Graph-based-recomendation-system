from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView
from graph_recsys.forms import PreferForm, TrackForm
from graph_recsys.models import Prefer, Genre, Track
from graph_recsys.services import (
    construct_graf,
    draw_graph,
    get_simrank_similarity,
    get_pagerank,
    make_recomentaions,
)
from users.models import User


def add_listener(request, pk):
    """
    функция добавления пользователя в listeners трека
    """
    track = get_object_or_404(Track, pk=pk)
    user = request.user
    if user not in track.listeners.all():
        track.listeners.add(user)

    track.save()
    return redirect(reverse("graph_recsys:main"))


def add_genre_to_prefer(request, pk):
    """
    функция добавления жанра в предпочтения
    """
    user = request.user
    if user.is_authenticated:
        genre = Genre.objects.get(pk=pk)
        if Prefer.objects.get(user=user):
            prefer = Prefer.objects.get(user=user)
            if genre not in prefer.genres.all():
                prefer.genres.add(genre)
            else:
                prefer.genres.remove(genre)
            prefer.save()
    return redirect(reverse("graph_recsys:main"))


def clear_play_list(request):
    """
    функция очистки плейлиста
    """
    user = request.user
    tracks = user.track_set.all()
    for track in tracks:
        track.listeners.remove(user)
        track.save()

    return redirect(reverse("graph_recsys:main"))


class TrackCreateVies(CreateView):
    """
    контроллер создания трека
    """

    model = Track
    form_class = TrackForm
    success_url = reverse_lazy("graph_recsys:main")


class TrackUpdateView(UpdateView):
    """
    контроллер обновления трека
    """

    model = Track
    form_class = TrackForm
    success_url = reverse_lazy("graph_recsys:main")

    def update(self):
        user = self.request.user
        if user.is_authenticated:
            track = self.object.save()
            if user not in track.listeners.all():
                track.listeners.add(user)


class PreferCreateView(CreateView):
    """
    контроллер создания предпочтений
    """

    model = Prefer
    form_class = PreferForm
    success_url = reverse_lazy("graph_recsys:main")

    def form_valid(self, form):
        context_data = self.get_context_data()
        if form.is_valid():
            prefer = form.save()
            prefer.user = self.request.user
            prefer.save()
            return super().form_valid(form)


class PreferUpdateView(UpdateView):
    """
    контроллер редактирования предпочтений
    """

    model = Prefer
    form_class = PreferForm
    success_url = reverse_lazy("graph_recsys:main")

    def form_valid(self, form):
        context_data = self.get_context_data()
        if form.is_valid():
            prefer = form.save()
            prefer.user = self.request.user
            prefer.save()
            return super().form_valid(form)


class MainPageView(TemplateView, LoginRequiredMixin):
    """
    контроллер главной страницы
    """

    template_name = "graph_recsys/main.html"
    success_url = reverse_lazy("recsys:main")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context_data["release"] = True
            user = User.objects.get(id=self.request.user.id)
            context_data["genres"] = Genre.objects.all()

            if Prefer.objects.filter(user=self.request.user).exists():
                context_data["prefers"] = Genre.objects.filter(
                    pk__in=[x.id for x in Prefer.objects.get(user_id=user).genres.all()]
                )
                context_data["pref"] = Prefer.objects.get(user_id=user)
                context_data["user_tracks"] = user.track_set.all()

                # simrank similarity
                simrank_similarity = get_simrank_similarity(construct_graf(user))
                context_data["simrank"] = simrank_similarity

                # pagerank
                pagerank_data = get_pagerank(construct_graf(user))
                context_data["recomendations"] = make_recomentaions(
                    pagerank_data, user, simrank_similarity, 3
                )

            else:
                context_data["prefers"] = None
        return context_data

    def get_form(self):
        user = self.request.user
        if user.is_authenticated:
            if Prefer.objects.filter(user=user).exists():
                return PreferForm(
                    initial={
                        "genres": Genre.objects.filter(
                            pk__in=Prefer.objects.get(user_id=user).genres.all()
                        )
                    }
                )
        return PreferForm


class StatisticsPageView(TemplateView, LoginRequiredMixin):
    """
    контроллер страницы статистики
    """

    template_name = "graph_recsys/statistics.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = User.objects.get(id=self.request.user.id)

            # simrank similarity
            simrank_similarity = get_simrank_similarity(construct_graf(user))
            context_data["simrank"] = simrank_similarity

            # pagerank
            pagerank_data = get_pagerank(construct_graf(user))

            context_data["tracks"] = pagerank_data["tracks"]
            context_data["genres"] = pagerank_data["genres"]
            # draw graph
            context_data["graph"] = draw_graph(construct_graf(user))
        return context_data
