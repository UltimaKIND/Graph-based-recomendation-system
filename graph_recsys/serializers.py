from rest_framework.serializers import ModelSerializer
from graph_recsys.models import Prefer


class PreferSerializer(ModelSerializer):
    """
    сериализатор модели предпочтений
    """

    class Meta:
        model = Prefer
        fields = ("genres",)
