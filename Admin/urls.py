from django.urls import path, include 
from rest_framework.routers import DefaultRouter 

from .views import UserProfileViewSet
from .views import SendMailViewSet 


router = DefaultRouter()

router.register(r'profile', UserProfileViewSet, basename='Profile')
router.register(r'send-mail', SendMailViewSet, basename='send-mail')

urlpatterns = [
    path('', include(router.urls)),
    # path('mail/', SendMailViewSet.as_view(), name='mail'), 
]
