from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    """
    сериализатор модели пользователя
    """

    class Meta:
        model = User
        fields = "__all__"


class OtherUserSerializer(ModelSerializer):
    """
    сериализатор модели пользователя
    """

    class Meta:
        model = User
        exclude = ("password", "last_name")