from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.sellers.models import Seller
from apps.sellers.serializers import SellerSerializer
from apps.shop.models import Product, Category
from apps.shop.serializers import ProductSerializer, CreateProductSerializer

tags = ["Sellers"]

class SellersView(APIView):
    serializer_class = SellerSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, partial=False)
        if serializer.is_valid():
            data = serializer.validated_data
            seller, _ = Seller.objects.update_or_create(user=user, defaults=data)
            user.account_type = 'SELLER'
            user.save()
            serializer = self.serializer_class(seller)
            return Response(data=serializer.data, status=201)
        else:
            return Response(data=serializer.errors, status=400)

class SellerProductsView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get_or_none(user=request.user, is_approved=True)
        if not seller:
            return Response(data= {"message": "Access denied"}, status=403)
        products = Product.objects.select_related("category", "seller", "seller__user").filter(seller=seller)
        serializer = self.serializer_class(products, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = CreateProductSerializer(data=request.data)
        seller = Seller.objects.get_or_none(user=request.user, is_approved=True)
        if not seller:
            return Response(data= {"message": "Access denied"}, status=403)
        if serializer.is_valid():
            data = serializer.validated_data
            print(data)
            category_slug = data.pop("category_slug", None)
            category = Category.objects.get_or_none(slug=category_slug)
            if not category:
                return Response(data= {"message": "Category not found"}, status=404)
            data['category'] = category
            data['seller'] = seller
            new = Product.objects.create(**data)
            serializer = self.serializer_class(new)
            return Response(data=serializer.data, status=201)
        else:
            return Response(data=serializer.errors, status=400)

