from api.pagination import CustomPageNumberPagination
from api.serializers.subscription_serializers import SubscriptionsSerializer
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import CreateDestroyViewSet

User = get_user_model()


class SubscriptionsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.request.user.following.all()


class SubscribeCreateDestroyViewSet(CreateDestroyViewSet):

    id_endpoint = 'user_id'
    model = User
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        return SubscriptionsSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        to_follow = self._get_entity_by_id()
        if to_follow == user:
            return Response({'error': 'you cannot follow yourself'},
                            status=status.HTTP_400_BAD_REQUEST)
        if to_follow in user.following.all():
            return Response(
                {'error': 'you\'re already following this account'},
                status=status.HTTP_400_BAD_REQUEST)
        user.following.add(to_follow)
        data = SubscriptionsSerializer(to_follow,
                                       context={'request': request}).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = request.user
        unfollow = self._get_entity_by_id()
        if unfollow not in user.following.all():
            return Response({'bad request': 'you don\'t follow this user'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.following.remove(unfollow)
        return Response(status=status.HTTP_204_NO_CONTENT)
