from rest_framework import mixins, viewsets
from rest_framework import filters

from .permissions import ReadonlyOrAdmin


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class RetrieveUpdateDeleteViewSet(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    pass


class PutExclude(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    http_method_names = ["get", "post", "patch", "delete"]


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (ReadonlyOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
