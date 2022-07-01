from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer


class CreateUserAPIView(APIView):
    """View de l'enregistrement d'un user"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """Méthode POST pour l'enregistrement d'un user"""
        user = request.data
        serializer = UserSerializer(data=user)
        print(f"\n{request.data}\n")
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
