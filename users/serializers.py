from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """Serializer du model User"""

    class Meta:
        model = User
        fields = [
            "id", "username", "password", "first_name", "last_name", "email",
        ]

    def create(self, validated_data):
        """Création d'un user en base de données"""
        user = User.objects.create_user(**validated_data)
        return user
