from rest_framework import viewsets, serializers, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout

from .models import AudioSegment, CharacterSet
from .serializers import AudioSegmentSerializer, CharacterSetSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"success": "User logged in"}, status=status.HTTP_200_OK)
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
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
    queryset = AudioSegment.objects.all()
    serializer_class = AudioSegmentSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# Add any additional views you may have below
