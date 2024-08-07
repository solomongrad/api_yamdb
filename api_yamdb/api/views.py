from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import CommentSerializer, TitleSerializer, ReviewSerializer
from reviews.models import Review, Title


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(title=self.get_title(), author=user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(review=self.get_review(), author=user)
