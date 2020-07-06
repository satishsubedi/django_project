from django.urls import path
from .views import SignupAPIView,LoginAPIView,PasswordChangeAPIView,UserProfileAPIView,UserProfileUpdateAPIView
urlpatterns = [
    path('signup/',SignupAPIView.as_view(),name='user_register'),
    path('login/', LoginAPIView.as_view(),name='login_api'),
    path('password/change/', PasswordChangeAPIView.as_view(),name='password_change'),
    path('profile/',UserProfileAPIView.as_view(),name = 'user_profile'),
    path('profile/update/<int:pk>/',UserProfileUpdateAPIView.as_view(),name = 'user_profile_update'),


 ]