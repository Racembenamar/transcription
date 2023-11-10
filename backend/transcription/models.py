from django.db import models
from django.contrib.auth.models import User

class CharacterSet(models.Model):
    characters = models.TextField()

    @staticmethod
    def get_default_characters():
        # Retrieve the first character set instance from the database
        try:
            return CharacterSet.objects.first().characters
        except AttributeError:
            # If there are no CharacterSet instances, you can return a default set
            # or handle the case as you see fit.
            return ""  # Returning an empty string as a placeholder

    def __str__(self):
        return self.characters

class AudioSegment(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    transcribed_text = models.TextField(blank=True)
    is_transcribed = models.BooleanField(default=False)
    transcribed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Audio Segment {self.id}"
