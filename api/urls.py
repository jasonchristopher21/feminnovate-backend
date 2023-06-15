from django.urls import path
from . import views

urlpatterns = [
    path('public', views.PublicView.as_view())
]