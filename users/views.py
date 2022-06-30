from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from users.serializers import UserSerializer


class CreateUserAPIView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        user = request.data
        serializer = UserSerializer(data=user)
        print(f"\n{request.data}\n")
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
