from django.shortcuts import render
from store.models import Product , Audience , ClothingType 
from store.serializer import ProductSerializer , AudienceSerializer , ClothingTypeSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny , IsAuthenticated


class AudienceListAPIView(generics.ListAPIView):
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer
    permission_classes = [AllowAny]


class ClothingTypeListAPIView(generics.ListAPIView):
    queryset = ClothingType.objects.all()
    serializer_class = ClothingTypeSerializer
    permission_classes = [AllowAny]

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductDetailListAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    def get_object(self):
        slug = self.kwargs['slug']
        return Product.objects.get(slug = slug)

