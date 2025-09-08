from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.common.utils import set_dict_attr
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
            category_data = data.pop('category')
            category_slug = category_data.get('slug')
            if not category_slug:
                return Response(data= {"message": "Category not found. ErrorCode: 5877"}, status=404)
            category = Category.objects.get_or_none(slug=category_slug)
            data['category'] = category
            data['seller'] = seller
            new = Product.objects.create(**data)
            serializer = self.serializer_class(new)
            return Response(data=serializer.data, status=201)
        else:
            return Response(data=serializer.errors, status=400)

class SellerProductView(APIView):
    serializer_class = CreateProductSerializer

    def get_obj(self, slug):
        product = Product.objects.get_or_none(slug=slug)
        return product

    def put(self, request, *args, **kwargs):
        product = self.get_obj(slug=kwargs['slug'])
        if not product:
            return Response(data= {"message": "Product not found"}, status=404)
        if product.seller != request.user.seller.first():
            return Response(data= {"message": "Access denied"}, status=403)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            category_data = data.pop('category')
            category_slug = category_data.get('slug')
            if not category_slug:
                return Response(data={"message": "Category not found. ErrorCode: 5877"}, status=404)
            category = Category.objects.get_or_none(slug=category_slug)
            data['category'] = category
            if data["price_current"] != product.price_current:
                data["price_old"] = product.price_current
            product = set_dict_attr(product, data)
            product.save()
            serializer = ProductSerializer(product)
            return Response(data=serializer.data, status=200)
        else:
            return Response(data=serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        product = self.get_obj(slug=kwargs['slug'])
        if not product:
            return Response(data= {"message": "Product not found"}, status=404)
        elif product.seller != request.user.seller.first():
            return Response(data= {"message": "Access denied"}, status=403)
        product.delete()
        return Response(data= {"message": "Product deleted"}, status=200)

