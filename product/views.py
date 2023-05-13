
from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .tasks import add
from .models import Product, Category,Month 
from .serializers import ProductSerializer, CategorySerializer,MonthSerializer
# from django.core.checks impo

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        dd = add.delay(1,2)
        return Response(serializer.data)
    

class CategoryList(APIView):
    def get(self,request):
        category = Category.objects.all()
        serialzer = CategorySerializer(category,many=True)
        return Response(serialzer.data)
    


class MonthList(APIView):
    def get(self,request):
        months = Month.objects.all()
        serialzer = MonthSerializer(months,many=True)
        return Response(serialzer.data)