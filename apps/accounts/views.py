from http import HTTPStatus

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.accounts.serializers import CreateUserSerializer, NewTokenObtainPairSerializer


class RegisterAPIView(APIView):
    serializer_class = CreateUserSerializer

    @extend_schema(
        summary="Register new user",
        tags=['auth']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "success"}, HTTPStatus.CREATED)
        return Response(serializer.errors, HTTPStatus.UNPROCESSABLE_ENTITY)


class NewTokenObtainPairView(TokenObtainPairView):
    serializer_class = NewTokenObtainPairSerializer