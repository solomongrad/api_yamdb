from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Title, Review
from django.db.models import Avg


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg("score"))["score__avg"]
        if rating:
            return int(rating)
        return None

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('author', 'title',)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'review',)
