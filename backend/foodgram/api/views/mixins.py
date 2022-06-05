from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet


class CreateDestroyViewSet(GenericViewSet,
                           CreateModelMixin, DestroyModelMixin):

    def _get_entity_by_id(self):
        pk = self.kwargs.get(self.id_endpoint)
        instance = get_object_or_404(self.model, pk=pk)
        return instance
