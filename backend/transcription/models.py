from django.db import models
from django.contrib.auth.models import User

class CharacterSet(models.Model):
    characters = models.TextField()

    def __str__(self):
        return "CharacterSet"

class AudioSegment(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    transcribed_text = models.TextField(blank=True)
    is_transcribed = models.BooleanField(default=False)
    transcribed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Audio Segment {self.id}"
