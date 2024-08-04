from rest_framework import serializers
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
    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)