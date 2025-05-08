from django.urls import path, include 

from xApiAuthentication.views import SignInView 
from xApiAuthentication.views import SignUpView
from xApiAuthentication.views import SignOutView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signout/', SignOutView.as_view(), name='signout'),
]
