from rest_framework import viewsets, serializers, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .models import AudioSegment, CharacterSet
from .serializers import AudioSegmentSerializer, CharacterSetSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .serializers import AudioFileUploadSerializer
from rest_framework.permissions import BasePermission

class IsTranscriber(permissions.BasePermission):
    """
    Custom permission to only allow users in the 'Transcribers' group.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Transcribers').exists()
     
class UserRegistrationView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AudioFileUploadView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, format=None):
        serializer = AudioFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            is_transcriber = user.groups.filter(name='Transcribers').exists()
            is_audio_uploader = user.groups.filter(name='Simple User').exists()

            return Response({
                "success": "User logged in", 
                "token": token.key,
                "is_transcriber": is_transcriber,
                "is_audio_uploader": is_audio_uploader
            })
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"success": "User logged out"}, status=status.HTTP_200_OK)

class AudioSegmentViewSet(viewsets.ModelViewSet):
    queryset = AudioSegment.objects.all()
    serializer_class = AudioSegmentSerializer

    def validate_transcription(self, value):
        character_set = CharacterSet.get_default_characters()
        if set(value).issubset(set(character_set.characters)):
            return value
        else:
            raise serializers.ValidationError("Transcription contains invalid characters.")

    class Meta:
        model = AudioSegment
        fields = '__all__'

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AudioUploaders').exists():
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        user = self.request.user
        if not user.groups.filter(name='Transcribers').exists():
            raise serializers.ValidationError("Not authorized to transcribe")

        if 'transcribed_text' in serializer.validated_data:
            transcribed_text = serializer.validated_data['transcribed_text']
            serializer.instance.transcribed_text = transcribed_text
            serializer.instance.save()

    def get_queryset(self):
        queryset = AudioSegment.objects.all()
        is_transcribed = self.request.query_params.get('is_transcribed', None)
        if is_transcribed is not None:
            is_transcribed = is_transcribed.lower() in ['true', '1']
            queryset = queryset.filter(is_transcribed=is_transcribed)
        return queryset

class CharacterSetViewSet(viewsets.ModelViewSet):
    queryset = CharacterSet.objects.all()
    serializer_class = CharacterSetSerializer

class AudioSegmentListCreateView(generics.ListCreateAPIView):
    queryset = AudioSegment.objects.all()
    serializer_class = AudioSegmentSerializer

class AudioSegmentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsTranscriber]
    queryset = AudioSegment.objects.all()
    serializer_class = AudioSegmentSerializer
    
    def get_serializer_context(self):
        context = super(AudioSegmentRetrieveUpdateView, self).get_serializer_context()
        return context
