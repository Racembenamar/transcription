from rest_framework import viewsets, permissions
from .models import AudioSegment, CharacterSet
from .serializers import AudioSegmentSerializer, CharacterSetSerializer

class AudioSegmentViewSet(viewsets.ModelViewSet):
    queryset = AudioSegment.objects.all()
    serializer_class = AudioSegmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned audio segments to those that have not been transcribed,
        by filtering against a `transcribed` query parameter in the URL.
        """
        queryset = AudioSegment.objects.all()
        transcribed = self.request.query_params.get('transcribed', None)
        if transcribed is not None:
            queryset = queryset.filter(transcribed=transcribed in ['True', 'true', '1'])
        return queryset

class CharacterSetViewSet(viewsets.ModelViewSet):
    queryset = CharacterSet.objects.all()
    serializer_class = CharacterSetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
