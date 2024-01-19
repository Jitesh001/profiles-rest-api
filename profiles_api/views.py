from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class HelloAPIView(APIView):

    def get(self, request, format=None):
        data = {'message':'this is response', 'data':['apple', 'banana']}
        return Response(data)
