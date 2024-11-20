from idlelib.debugger_r import wrap_info

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, FormView, DeleteView
from networkx.classes import neighbors
from rest_framework.generics import CreateAPIView, UpdateAPIView  # type: ignore
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet  # type: ignore

from graph_recsys.forms import PreferForm, TrackForm
from graph_recsys.models import Prefer, Genre, Track
from graph_recsys.serializers import PreferSerializer
from graph_recsys.services import construct_graf, draw_graph, make_recomendation, get_data, get_simrank_similarity, \
    get_pagerank, get_knn, get_neighbors, get_track, make_recomentaions
from users.models import User

def add_listener(request, pk):
    """
    контроллер публикации поста
    """
    track = get_object_or_404(Track, pk=pk)
    user = request.user
    if user not in track.listeners.all():
        track.listeners.add(user)

    track.save()
    return redirect(reverse('graph_recsys:main'))

def add_genre_to_prefer(request, pk):
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
    return redirect(reverse('graph_recsys:main'))

def clear_play_list(request):
    user = request.user
    tracks = user.track_set.all()
    for track in tracks:
        track.listeners.remove(user)
        track.save()

    return redirect(reverse('graph_recsys:main'))






class TrackCreateVies(CreateView):
    model = Track
    form_class = TrackForm
    success_url = reverse_lazy('graph_recsys:main')

class TrackUpdateView(UpdateView):
    model = Track
    form_class = TrackForm
    success_url = reverse_lazy('graph_recsys:main')

    def update(self):
        user = self.request.user
        if user.is_authenticated:
            track = self.object.save()
            if user not in track.listeners.all():
                track.listeners.add(user)




class PreferCreateView(CreateView):
    model = Prefer
    form_class = PreferForm
    success_url = reverse_lazy('graph_recsys:main')

    def form_valid(self, form):
        context_data = self.get_context_data()
        if form.is_valid() :
            prefer = form.save()
            prefer.user = self.request.user
            prefer.save()
            return super().form_valid(form)

    #serializer_class = PreferSerializer
    #queryset = Prefer.objects.all()
    #permission_classes = [IsAuthenticated]
    #def perform_create(self, serializer):
    #    prefer = serializer.save()
    #    prefer.user = self.request.user
    #    prefer.save()

class PreferUpdateView(UpdateView):

    model = Prefer
    form_class = PreferForm
    success_url = reverse_lazy('graph_recsys:main')

    def form_valid(self, form):
        context_data = self.get_context_data()
        if form.is_valid() :
            prefer = form.save()
            prefer.user = self.request.user
            prefer.save()
            return super().form_valid(form)

class MainPageView(TemplateView, LoginRequiredMixin):
    """
    контроллер для главной страницы
    """
    template_name = 'graph_recsys/main.html'
    success_url = reverse_lazy('recsys:main')


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context_data['release'] = True
            user = User.objects.get(id=self.request.user.id)
            context_data['genres'] = Genre.objects.all()

            if Prefer.objects.filter(user=self.request.user).exists():
                context_data['prefers'] = Genre.objects.filter(pk__in=[x.id for x in Prefer.objects.get(user_id=user).genres.all()])
                context_data['pref'] = Prefer.objects.get(user_id=user)
                context_data['user_tracks'] = user.track_set.all()


                # recomendation from cosine_dist (collaborative filtration)
                # не работает
                # zero_division_error пока нет user-item связи
                #if user.track_set.exists():
                #context_data['simrank'] = make_recomendation(user)
                #else:
                #    context_data['simrank'] = None

                # simrank similarity
                simrank_similarity = get_simrank_similarity(construct_graf(user))
                context_data['simrank'] = simrank_similarity

                #knn
                #knn = get_knn(construct_graf(user))
                #context_data['coll'] = knn

                # pagerank
                pagerank_data = get_pagerank(construct_graf(user))
                context_data['recomendations'] = make_recomentaions(pagerank_data, user, simrank_similarity, 3)



                #context_data['coll'] = {key:value for key, value in pagerank_data.items() if key.genre.name in [x.name for x in Prefer.objects.get(user_id=user).genres.all()]}


                # context_data['coll'] = get_data()
                # context_data['graph'] = construct_graf()
                # отрисовка графа
                # context_data['test'] = draw_graph(graph=None)
            else:
                context_data['prefers'] = None
        return context_data

    def get_form(self):
        user = self.request.user
        if user.is_authenticated:
        #return PreferForm
        #return PreferForm(*{'initial': Genre.objects.filter(pk__in=[x.id for x in Prefer.objects.get(user_id=user).genres.all()]), 'prefix': None})

            if Prefer.objects.filter(user=user).exists():
                return PreferForm(initial={'genres':Genre.objects.filter(pk__in=Prefer.objects.get(user_id=user).genres.all())})
        return PreferForm


class StatisticsPageView(TemplateView, LoginRequiredMixin):
    template_name = 'graph_recsys/statistics.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = User.objects.get(id=self.request.user.id)


            # simrank similarity
            simrank_similarity = get_simrank_similarity(construct_graf(user))
            context_data['simrank'] = simrank_similarity
            pagerank_data = get_pagerank(construct_graf(user))
            context_data['tracks'] = pagerank_data['tracks']
            context_data['genres'] = pagerank_data['genres']
            context_data['graph'] = draw_graph(construct_graf(user))
        return context_data
