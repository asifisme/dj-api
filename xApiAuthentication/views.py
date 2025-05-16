from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions 

from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework_simplejwt.views import TokenRefreshView  
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model  
from django.contrib.auth import authenticate, login 

from .serializers import SignInSerializer 
from .serializers import SingUpSerializer



User = get_user_model() 


class SignUpView(APIView):
    """ Sign up view """
    permission_classes      = [permissions.AllowAny] 

    def post(self, request):
        serializer        = SingUpSerializer(data=request.data) 

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    """ Sign in view """
    permission_classes      = [permissions.AllowAny] 

    def post(self, request):
        serializer        = SignInSerializer(data=request.data) 

        if not serializer.is_valid():
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        username_or_email = serializer.validated_data['username_or_email']
        password          = serializer.validated_data['password']



        if not username_or_email or not password:
            return Response({"error": "Username or email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = None

        if "@" in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
                
        if not user.check_password(password):
            return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(request, username=user.email, password=password) 

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
                return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class SignOutView(APIView):
    """ Log out the user by blacklisting the refresh token """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)