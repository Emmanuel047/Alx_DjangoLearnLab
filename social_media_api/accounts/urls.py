from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
    # Direct follow/unfollow paths as specified
    path('follow/<int:user_id>/', views.UserViewSet.as_view({'post': 'followuser'}), name='follow_user'),
    path('unfollow/<int:user_id>/', views.UserViewSet.as_view({'post': 'unfollowuser'}), name='unfollow_user'),
]
