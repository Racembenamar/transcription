from rest_framework import viewsets
from .models import AudioSegment, CharacterSet
from .serializers import AudioSegmentSerializer, CharacterSetSerializer

class AudioSegmentViewSet(viewsets.ModelViewSet):
    queryset = AudioSegment.objects.all()
    serializer_class = AudioSegmentSerializer

class CharacterSetViewSet(viewsets.ModelViewSet):
    queryset = CharacterSet.objects.all()
    serializer_class = CharacterSetSerializer
