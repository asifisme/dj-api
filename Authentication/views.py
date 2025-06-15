import logging 
import controller 
from django.utils import timezone 
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions 

from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import generics 

from django.contrib.auth import get_user_model  
from django.contrib.auth import authenticate, login 
from django.core.mail import send_mail 
from django.conf import settings 
from django.contrib.auth.tokens import PasswordResetTokenGenerator 



from .serializers import SignInSerializer 
from .serializers import SingUpSerializer
from .serializers import ChangePasswordSerializer 
from .serializers import ResetPasswordRequestSerializer
from .serializers import ResetPasswordSerializer 

logger = logging.getLogger(__name__) 

User = get_user_model() 

if controller.GLOBAL_EMAIL_SYSTEM:
    def send_global_email(subject, message, recipient_list):
        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False) 





class SignUpView(APIView):
    """ Sign up view """
    permission_classes      = [permissions.AllowAny] 


    def post(self, request):
        serializer          = SingUpSerializer(data=request.data) 


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        
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

            # send user mail after successful login 
            if controller.GLOBAL_EMAIL_SYSTEM:
                subject = "Security Alert: Successful Sign-In to Your Account"
                message = f"""
                Hi {user.first_name or user.username},

                We noticed a successful sign-in to your account.

                Details:
                - Username: {user.username}
                - Email: {user.email}
                - Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)

                If this was you, no further action is needed.

                If you didn’t sign in, please secure your account immediately by resetting your password or contacting our support team.

                Thank you for using our service.

                Best regards,  
                The [xApi] Team
                """
                send_global_email(subject, message, [user.email])

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

            if controller.GLOBAL_EMAIL_SYSTEM: 
            # send user mail after successful logout 
                subject = "Security Alert: Successful Sign-Out from Your Account"
                message = f"""
                Hi {request.user.first_name or request.user.username},
                We noticed a successful sign-out from your account.
                Details:
                - Username: {request.user.username}
                - Email: {request.user.email}
                - Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)
                If this was you, no further action is needed.
                If you didn’t sign out, please secure your account immediately by resetting your password or contacting our support team.
                Thank you for using our service.
                Best regards,
                The [xApi] Team
                """
                send_global_email(subject, message, [request.user.email]) 

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = ChangePasswordSerializer 

    def post(self, request):
        serializer = self.serializer_class(data=request.data) 

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
        old_password = serializer.validated_data['old_password'] 
        new_password = serializer.validated_data['new_password'] 
        confirm_password = serializer.validated_data['confirm_password'] 

        if not request.user.check_password(old_password):
            return Response({"message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST) 
        
        if new_password != confirm_password:
            return Response({"message": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST) 
        
        request.user.set_password(new_password)
        request.user.save() 

        logger.info(f"Password for user {request.user.username} has been changed.")

        if controller.GLOBAL_EMAIL_SYSTEM: 
            subject = "Your Password Has Been Changed Successfully"
            message = f"""
            Hi {request.user.first_name or request.user.username},
            Your password has been changed successfully.
            If you did not make this change, please contact our support team immediately.
            Thank you for using our service.
            Best regards,
            The xApi Team
            """
            send_global_email(subject, message, [request.user.email]) 

        return Response({"message": "Password has been changed successfully"}, status=status.HTTP_200_OK)




class ResetPasswordRequestView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny] 
    serializer_class = ResetPasswordRequestSerializer 

    def post(self, request): 
        serializer = self.serializer_class(data=request.data) 

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
        username_or_email = serializer.validated_data['username_or_email'] 


        user = User.objects.filter(email=username_or_email).first() 

        if not user: 
            user = user or User.objects.filter(username=username_or_email).first()

        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND) 
        
        token = PasswordResetTokenGenerator().make_token(user) 

        reset_link = request.build_absolute_uri(f"/api/v1/reset-password-confirm/{user.username}/{token}/")

        if  controller.GLOBAL_EMAIL_SYSTEM: 
            subject = "Password Reset Request"
            message = f"""
            Hi {user.first_name or user.username},

            We received a request to reset your password. If you did not make this request, please ignore this email.

            To reset your password, please click the link below:

            {reset_link}

            If you have any questions or need further assistance, feel free to contact our support team.

            Thank you for using our service.

            Best regards,
            The xApi Team
            """
            send_global_email(subject, message, [user.email]) 

        return Response({"message": "Password reset link has been sent to your email"}, status=status.HTTP_200_OK) 

    


class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request, uid, token):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=uid)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST) 

        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if new_password != confirm_password:
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        

        user.set_password(new_password)
        user.save() 


        logger.info(f"Password for user {user.username} has been reset.")

        if  controller.GLOBAL_EMAIL_SYSTEM: 
            subject = "Your Password Has Been Reset Successfully"
            message = f"""
            Hi {user.first_name or user.username},
            Your password has been reset successfully.
            If you did not request this change, please contact our support team immediately.
            Thank you for using our service.
            Best regards,
            The xApi Team
            """
            send_global_email(subject, message, [user.email])

        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)





