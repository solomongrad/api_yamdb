from rest_framework import mixins, viewsets, filters

from .permissions import ReadonlyOrAdmin


class PutExclude(viewsets.ModelViewSet):
    """Вьюсет предоставляющий доступ к GET, POST, PATCH И DELETE запросам."""

    http_method_names = ["get", "post", "patch", "delete"]


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Вьюсет состоящий из нескольких миксинов.
    Позволяет получить список объектов, создать объект или удалить объект.
    """
    permission_classes = (ReadonlyOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
