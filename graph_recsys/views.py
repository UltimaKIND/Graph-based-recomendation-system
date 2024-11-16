from idlelib.debugger_r import wrap_info

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, FormView
from networkx.classes import neighbors
from rest_framework.generics import CreateAPIView, UpdateAPIView  # type: ignore
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet  # type: ignore

from graph_recsys.forms import PreferForm
from graph_recsys.models import Prefer, Genre, Track
from graph_recsys.serializers import PreferSerializer
from graph_recsys.services import construct_graf, draw_graph, make_recomendation, get_data, get_simrank_similarity, \
    get_pagerank, get_knn, get_neighbors, get_track
from users.models import User



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

class MainPageView(FormView):
    """
    контроллер для главной страницы
    """
    template_name = 'graph_recsys/main.html'
    success_url = reverse_lazy('recsys:main')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = User.objects.get(email=self.request.user.email)
        if Prefer.objects.filter(user=self.request.user).exists():
            pass
            # context_data['prefers'] = Genre.objects.filter(pk__in=[x.id for x in Prefer.objects.get(user_id=user).genres.all()])
            # context_data['pref'] = Prefer.objects.get(user_id=user)

            # recomendation from cosine_dist (collaborative filtration)
            # zero_division_error пока нет user-item связи
            # context_data['collaborative'] = make_recomendation(user)

            # simrank similarity
            #simrank_similarity = get_simrank_similarity(construct_graf(user))
            #context_data['simrank'] = simrank_similarity

            #knn
            #knn = get_knn(construct_graf(user))
            #context_data['coll'] = knn

            # pagerank
            #pagerank_data = get_pagerank(construct_graf(user))
            #tracks_for_recomendation = get_track(pagerank_data, user)
            #context_data['page_rank'] = tracks_for_recomendation


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
        #return PreferForm
        #return PreferForm(*{'initial': Genre.objects.filter(pk__in=[x.id for x in Prefer.objects.get(user_id=user).genres.all()]), 'prefix': None})

        #if Prefer.objects.filter(user=user).exists():
        #    return PreferForm(initial={'genres':Genre.objects.filter(pk__in=Prefer.objects.get(user_id=user).genres.all())})
        return PreferForm

