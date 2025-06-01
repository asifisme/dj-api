from django.urls import path, include 

from .views import SignInView 
from .views import SignUpView
from .views import SignOutView
from .views import ResetPasswordRequestView 
from .views import ResetPasswordConfirmView 
from .views import ChangePasswordView 


urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signout/', SignOutView.as_view(), name='signout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'), 
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset_password'), 
    path('reset-password-confirm/<str:uid>/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'), 
]
