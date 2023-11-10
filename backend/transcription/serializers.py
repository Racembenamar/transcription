from rest_framework import serializers
from .models import AudioSegment, CharacterSet

class AudioSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioSegment
        fields = ['id', 'audio_file', 'transcribed_text', 'is_transcribed', 'transcribed_by']

class CharacterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSet
        fields = ['characters']
