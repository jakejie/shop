import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from backend.helpers import InputErrorMessage, JSONResponse
from .models import Product, ProductSerializer


# Create your views here.
class ProductList(APIView):
    def get(self, request, format=None):
        """
        预期：
        {
            "data": [
            {
                    "id": 1,
                    "name": "jacket1",
                    "price": "122.00",
                    "img": "media/jacket1.png"
                }
            ],
            "code": 200
        }
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JSONResponse(serializer.data)

    def post(self, request):
        """
        希望的输入：(UTF-8 coded)
            {
                "name": "shoes",
                "price": 324.10,
                "img": "media/jacket1.png"
            }
        """
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return InputErrorMessage("Invalid JSON body")
        if "name" not in data:
            return InputErrorMessage("Product name not provide.")
        if Product.objects.filter(name=data["name"]).exists():
            return InputErrorMessage("Product name is used.")
        if "price" not in data:
            return InputErrorMessage("Product price not provide.")
        if "img" not in data:
            return InputErrorMessage("Product image not provide.")
        products = Product.objects.create(
            name=data["name"], price=data["price"], img=data["img"])
        products.save()
        return JSONResponse({
            "code": 200,
            "message": "Success!",
        })