from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioSegmentViewSet, CharacterSetViewSet, LoginView, logout_view
from . import views  # Add this import

router = DefaultRouter()
router.register(r'audio_segments', AudioSegmentViewSet)
router.register(r'character_sets', CharacterSetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('audio_segments/', views.AudioSegmentListCreateView.as_view(), name='audio-segment-list-create'),
    path('audio_segments/<int:pk>/', views.AudioSegmentRetrieveUpdateView.as_view(), name='audio-segment-retrieve-update'),
]
