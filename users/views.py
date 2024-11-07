from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from graph_recsys.models import UserNode
from users.models import User
from users.permissions import IsModer, IsOwner, IsSelfUser
from users.serializers import UserSerializer, OtherUserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user_node = UserNode(email=user.email)
        user.set_password(user.password)
        user.save()
        user_node.save()


    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsAuthenticated,)
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsSelfUser]

        return super().get_permissions()

    def get_serializer_class(self):
        if (
            self.action in ["create", "update", "partial_update"]
            or self.action == "retrieve"
            and self.request.user == super().get_object()
        ):
            self.serializer_class = UserSerializer
        else:
            self.serializer_class = OtherUserSerializer
        return self.serializer_class