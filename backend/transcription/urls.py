from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioSegmentViewSet, CharacterSetViewSet, LoginView, logout_view

router = DefaultRouter()
router.register(r'audio_segments', AudioSegmentViewSet)
router.register(r'character_sets', CharacterSetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
