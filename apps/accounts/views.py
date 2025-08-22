from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.accounts.serializers import CreateUserSerializer, NewTokenObtainPairSerializer


class RegisterAPIView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "success"}, HTTPStatus.CREATED)
        return Response(serializer.errors, HTTPStatus.UNPROCESSABLE_ENTITY)


class NewTokenObtainPairView(TokenObtainPairView):
    serializer_class = NewTokenObtainPairSerializer