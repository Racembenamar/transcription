from rest_framework import viewsets, permissions
from .models import AudioSegment, CharacterSet
from .serializers import AudioSegmentSerializer, CharacterSetSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"success": "User logged in"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"success": "User logged out"}, status=status.HTTP_200_OK)


class AudioSegmentViewSet(viewsets.ModelViewSet):
    queryset = AudioSegment.objects.all()
    serializer_class = AudioSegmentSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned audio segments to those that have not been transcribed,
        by filtering against a `transcribed` query parameter in the URL.
        """
        queryset = AudioSegment.objects.all()
        is_transcribed = self.request.query_params.get('is_transcribed', None)
        if is_transcribed is not None:
            # Convert the query parameter to a boolean
            is_transcribed = is_transcribed.lower() in ['true', '1']
            queryset = queryset.filter(is_transcribed=is_transcribed)
        return queryset

class CharacterSetViewSet(viewsets.ModelViewSet):
    queryset = CharacterSet.objects.all()
    serializer_class = CharacterSetSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]


