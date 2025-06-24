import google.generativeai as genai 
from django.conf import settings 
from django.utils import timezone 

from rest_framework.response import Response 
from rest_framework import status 
from rest_framework import viewsets 
from rest_framework import permissions 
from rest_framework.decorators import action


from .models import ChatSession 
from .models import ChatMessage 

from .serializers import ChatSessionSerializer
from .serializers import ChatMessageSerializer 
from core.core_permissions import IsOwnerStaffOrSuperUser 

genai.configure(api_key=settings.GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')



class ChatSessionViewSet(viewsets.ModelViewSet):
    """ ViewSet for handling chat sessions. """
    queryset            = ChatSession.objects.all()
    serializer_class    = ChatSessionSerializer
    permission_classes  = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser] 
    
    def create(self, request, *args, **kwargs):
        user = request.user
        new_session = request.data.get("new_session", False)
        today = timezone.now().date()

        # Check for today's session if not forcing new session
        if not new_session:
            session = ChatSession.objects.filter(author=user, created__date=today).first()
            if session:
                serializer = self.get_serializer(session)
                return Response(
                    {"message": "Today's session already exists.", "session": serializer.data},
                    status=status.HTTP_200_OK
                )

        # Create new session
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user, title=request.data.get("title", "New Session"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        user = self.request.user 
        qs = super().get_queryset()

        if user.is_superuser or user.is_staff:
            return qs 
            
        
        return qs.filter(author=user)



    @action(methods=['delete'],  detail=False, url_path='delete-first')
    def delete_first(self, request):
        user = request.user 
        first_session = ChatSession.objects.filter(author=user).order_by('created').first() 

        if not first_session:
            return Response({"detail" : "No session found"}, status=status.HTTP_404_NOT_FOUND)
        
        first_session.delete()
        return Response({"message": "First Session Delete"}, status=status.HTTP_204_NO_CONTENT) 
    



def ask_gemini(prompt: str) -> str: 
    """ Helper function """ 
    try:
        response = model.generate_content(prompt) 
        return response.text
    except Exception as e: 
        return str(e)




class ChatBotViewSet(viewsets.ModelViewSet):
    """ ViewSet for handling chat messages. """ 
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user = self.request.user 
        qs = super().get_queryset()

        if user.is_superuser or user.is_staff:
            return qs 
            
        
        return qs.filter(session__author=user)


    def create(self, request, *args, **kwargs):
        """ Handle chat message creation and response generation. """
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_type = serializer.validated_data['message_type']
        prompt = serializer.validated_data['prompt']

        # Get the current session for the user
        current_session = ChatSession.objects.filter(author=request.user).order_by('-created').first()
        if not current_session:
            return Response({"detail": "No active chat session found for user."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate response using Gemini
        answer = ask_gemini(prompt)

        # Save the chat message with the generated answer and required fields
        serializer.save(
            session=current_session,
            message_type=message_type,
            answer=answer,
            role='user'  
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """ List all chat messages. """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
