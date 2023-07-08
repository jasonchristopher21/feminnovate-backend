from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('public', views.PublicView.as_view()),
    path('auth/register/', views.RegisterUserView.as_view()),
    path('auth/login/', views.JwtView.as_view()),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<str:username>/', views.UserView.as_view()),
]

