from django.core.management import BaseCommand
from graph_recsys.models import UserNode

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        nodes_to_create = [
            {"email": "test_1@sky.pro"}
        ]
        for node in nodes_to_create:
            UserNode(**node).save()
