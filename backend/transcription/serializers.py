from rest_framework import serializers
from .models import AudioSegment, CharacterSet
from .validators import validate_transcription
from django.contrib.auth.models import User
from rest_framework import serializers

class AudioFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioSegment
        fields = ['audio_file']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email'] 
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AudioSegmentSerializer(serializers.ModelSerializer):
    transcribed_text = serializers.CharField(validators=[validate_transcription])
    transcribed_by_username = serializers.SerializerMethodField()  

    class Meta:
        model = AudioSegment
        fields = ['id', 'audio_file', 'transcribed_text', 'is_transcribed', 'transcribed_by', 'transcribed_by_username']
    
    def get_transcribed_by_username(self, obj):
        return obj.transcribed_by.username if obj.transcribed_by else None
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if 'transcribed_text' in validated_data and not user.is_anonymous:
            instance.transcribed_by = user
            instance.is_transcribed = True

        return super(AudioSegmentSerializer, self).update(instance, validated_data)
    
    def save(self, **kwargs):
        user = self.context['request'].user
        if not user.is_anonymous:
            self.validated_data['transcribed_by'] = user

        return super(AudioSegmentSerializer, self).save(**kwargs)


class CharacterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSet
        fields = ['characters']
