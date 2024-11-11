from idlelib.debugger_r import wrap_info

from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, FormView
from rest_framework.generics import CreateAPIView, UpdateAPIView  # type: ignore
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet  # type: ignore

from graph_recsys.forms import PreferForm
from graph_recsys.models import Prefer, Genre
from graph_recsys.serializers import PreferSerializer
from graph_recsys.services import get_recomendation


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
    form_class = PreferForm
    success_url = reverse_lazy('recsys:main')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if Prefer.objects.filter(user=self.request.user).exists():
            context_data['prefers'] = Genre.objects.filter(pk__in=[x.genre_id for x in Prefer.objects.get(user_id=user).genres.constrained_target])
            context_data['pref'] = Prefer.objects.get(user_id=user)
            context_data['test'] = get_recomendation(user)
        else:
            context_data['prefers'] = None
        return context_data
