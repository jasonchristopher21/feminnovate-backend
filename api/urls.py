from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('auth/login/', views.JwtView.as_view()),
    path('auth/register/', views.RegisterUserView.as_view()),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('company/', views.CompanyRegisterView.as_view()),
    path('company/<int:id>/', views.CompanyRetrieveView.as_view()),
    path('job/', views.JobListView.as_view()),
    path('job/<int:id>/', views.JobDetailView.as_view()),
    path('public/', views.PublicView.as_view()),
    path('user/', views.UserView.as_view()),
    path('user/<str:username>/', views.UserView.as_view()),
    path('save/job/', views.SaveJobView.as_view()),
    path('work_experience/', views.WorkExperienceRegisterView.as_view()),
    path('work_experience/<int:id>/', views.WorkExperienceRetrieveView.as_view()),
    path('save/work_experience/', views.SaveWorkExperienceView.as_view()),
    path('workshop/', views.WorkshopRegisterView.as_view()),
    path('workshop/<int:id>/', views.WorkshopRetrieveView.as_view()),
    path('save/workshop/', views.SaveWorkshopView.as_view()),
    path('user/<str:username>/saved_jobs/', views.RetrieveSavedJobsView.as_view()),
    path('user/<str:username>/saved_workshops/', views.RetrievedSavedWorkshopsView.as_view()),
]
