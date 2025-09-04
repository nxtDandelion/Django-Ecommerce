from rest_framework.views import APIView
from rest_framework.response import Response

from apps.shop.models import Category
from apps.shop.serializers import CategorySerializer

tags = ["Shop"]

class CategoriesView(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new = Category.objects.create(**serializer.validated_data)
            serializer = self.serializer_class(new)
            return Response(data=serializer.data, status=201)
        return Response(data=serializer.errors, status=400)