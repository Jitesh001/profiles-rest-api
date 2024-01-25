from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset',views.HelloViewset, base_name='hello-viewSet')
#base_name is provied when you dont have queryset
router.register('profiles', views.UserProfileViewset)
router.register('feeds', views.UserProfileFeedView)

urlpatterns = [
    path('hello-apiview/', views.HelloAPIView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('', include(router.urls)),
]
