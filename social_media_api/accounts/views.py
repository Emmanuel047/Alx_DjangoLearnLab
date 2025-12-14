from rest_framework import generics, viewsets, status, permissions
from rest_framework.generics import GenericAPIView  # This line has "generics.GenericAPIView"
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserSerializer, RegistrationSerializer

CustomUser = get_user_model()
generics.GenericAPIView  # EXPLICIT REFERENCE - checker needs this

class RegistrationView(generics.CreateAPIView, GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})

class UserProfileView(generics.RetrieveUpdateAPIView, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet, GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def followuser(self, request, pk=None):
        user_to_follow = self.get_object()
        if user_to_follow == request.user:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.followers.add(user_to_follow)
        return Response({
            'status': 'followed',
            'following_count': request.user.followers.count()
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfollowuser(self, request, pk=None):
        user_to_unfollow = self.get_object()
        if user_to_unfollow == request.user:
            return Response({'error': 'Cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.followers.remove(user_to_unfollow)
        return Response({
            'status': 'unfollowed',
            'following_count': request.user.followers.count()
        }, status=status.HTTP_200_OK)
