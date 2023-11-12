from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CharacterSet(models.Model):
    characters = models.TextField()

    @staticmethod
    def get_default_characters():
        # Retrieve the first character set instance from the database
        try:
            return CharacterSet.objects.first()
        except CharacterSet.DoesNotExist:
            # If there are no CharacterSet instances, you can return a default set
            # or handle the case as you see fit.
            return None  # Returning None when no instances are found
            
    def __str__(self):
        return self.characters

class AudioSegment(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    transcribed_text = models.TextField(blank=True)
    is_transcribed = models.BooleanField(default=False)
    transcribed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Audio Segment {self.id}"


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)