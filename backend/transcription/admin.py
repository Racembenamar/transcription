# transcription/admin.py
from django.contrib import admin
from .models import AudioSegment, CharacterSet

admin.site.register(AudioSegment)
admin.site.register(CharacterSet)
