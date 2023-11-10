from rest_framework import serializers
from .models import AudioSegment, CharacterSet
from .validators import validate_transcription

class AudioSegmentSerializer(serializers.ModelSerializer):
    transcribed_text = serializers.CharField(validators=[validate_transcription])

    class Meta:
        model = AudioSegment
        fields = ['id', 'audio_file', 'transcribed_text', 'is_transcribed', 'transcribed_by']

class CharacterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSet
        fields = ['characters']
