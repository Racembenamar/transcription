from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioSegmentViewSet, CharacterSetViewSet

router = DefaultRouter()
router.register(r'audio_segments', AudioSegmentViewSet)
router.register(r'character_sets', CharacterSetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
