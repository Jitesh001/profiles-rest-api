from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from profiles_api import serializers, models, permissions


# Create your views here.
class HelloAPIView(APIView):

    serializer_class = serializers.HelloAPISerializer

    def get(self, request, format=None):
        data = {'message':'this is response', 'data':['apple', 'banana']}
        return Response(data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            print(serializer.validated_data)
            name = serializer.validated_data.get('name')
            msg = f'Hello {name}!!'
            return Response({'message':msg})
        else:
            # name_errors = serializer.errors.get('name', [])
            # if name_errors:
            #     err_msg = str(name_errors[0])
            #     code = name_errors[0].code
            #     print(err_msg, code)d
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({'msg':'PUT'})

    def patch(self, request, pk=None):
        return Response({'msg':'PATCH'})

    def delete(self, request, pk=None):
        return Response({'msg':'DELETE'})


class HelloViewset(viewsets.ViewSet):
    serializer_class = serializers.HelloAPISerializer

    def list(self, request):
        data = {'apple':200, 'mango':394}
        return Response(data)

    # @action(detail=False, methods=['get'])
    # def getMessage(self, request):
    #     return Response({'msg':'It worked'})
    #requires modelSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            msg = f'How are you? {name}'
            return Response({'msg':msg})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({'msg':'Retrieve'})

class UserProfileViewset(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'email']

class UserLoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class UserProfileFeedView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer 
    permission_classes = [permissions.UpdateOwnStatus, IsAuthenticatedOrReadOnly]
    queryset = models.ProfileFeedItem.objects.all()    
    
    def perform_create(self, serializer):
        user_profile = getattr(self.request, 'user', None)

        # Check if user_profile is an instance of UserProfile
        if user_profile and isinstance(user_profile, models.UserProfile):
            serializer.save(user_profile=user_profile)
        else:
            # Handle the case where user_profile is not a valid instance
            # You may want to log a warning or take appropriate action
            raise AssertionError("Invalid user profile or user not authenticated.")
