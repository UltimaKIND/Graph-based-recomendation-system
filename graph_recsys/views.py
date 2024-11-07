from multiprocessing.context import AuthenticationError

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from graph_recsys.models import *
from django.views.decorators.csrf import csrf_exempt
import json





class set_prefers(APIView):
    def post(self, request):
        user = self.request.user



