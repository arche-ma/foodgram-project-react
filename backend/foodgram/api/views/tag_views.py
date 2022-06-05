from api.serializers.tag_serializers import TagSerializer
from recipes.models import Tag
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]
