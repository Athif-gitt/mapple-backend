from rest_framework import serializers
from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "user", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 nd 5"
            )
        return value
    
    def validate(self, data):
        user = self.context["request"].user
        product = self.context["product"]

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(
                "Already reviewed"
            )
        return data
