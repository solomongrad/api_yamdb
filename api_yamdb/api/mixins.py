from rest_framework import mixins, viewsets, filters

from .permissions import ReadonlyOrAdmin


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Вьюсет предоставляющий доступ к GET и POST запросам.
    К созданию объекта или получению списка объектов.
    """

    pass


class RetrieveUpdateDeleteViewSet(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    """
    Вьюсет состоящий из нескольких миксинов.
    Позволяет получить объект в одном экземпляре,
    изменить объект или удалить его.
    """

    pass


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
