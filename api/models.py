from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import (
    CASCADE,
    DO_NOTHING,
    PROTECT,
    RESTRICT,
    SET,
    SET_DEFAULT,
    SET_NULL,
    ProtectedError,
    RestrictedError,
)
from api.enums import JobType, Experience

# Create your models here.
class BaseModel(models.Model):
    """
    Base model to be used for all models (except User)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(BaseModel):
    """
    Model to store user profile information
    """
    user = models.OneToOneField(User, on_delete=PROTECT, primary_key=True)
    name = models.CharField(max_length=155)
    description = models.CharField(max_length=155, blank=True)
    picture = models.URLField(max_length=155, blank=True)
    
    saved_jobs = models.ManyToManyField('Job', blank=True)
    saved_experiences = models.ManyToManyField('WorkExperience', blank=True)
    saved_workshops = models.ManyToManyField('Workshop', blank=True)

class Company(BaseModel):
    """
    Model to store company profile information
    """
    name = models.CharField(max_length=155)
    description = models.TextField()
    picture = models.URLField(max_length=155, blank=True)
    website = models.URLField(max_length=155, blank=True)

class Job(BaseModel):
    """
    Model to store job information
    """
    title = models.CharField(max_length=155)
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=CASCADE)
    salary = models.PositiveIntegerField(blank=True)
    location = models.CharField(max_length=155, blank=True)
    job_type = models.CharField(max_length=10, choices=JobType.choices, default=JobType.FULL_TIME, blank=True)
    experience = models.CharField(max_length=3, choices=Experience.choices, default=Experience.BETWEEN_1_2, blank=True)
    is_active = models.BooleanField(default=True)
    website = models.URLField(max_length=155, blank=True)

class WorkExperience(BaseModel):
    """
    Model to store work experience information
    """
    company = models.ForeignKey(Company, on_delete=CASCADE)
    role = models.CharField(max_length=155)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()

class Workshop(BaseModel):
    """
    Model to store workshop information
    """
    organizer = models.ForeignKey(Company, on_delete=CASCADE)
    title = models.CharField(max_length=155)
    description = models.TextField(blank=True)
    start_time = models.DateField(blank=True)
    end_time = models.DateField(blank=True)
    location = models.CharField(max_length=155, blank=True)
    website = models.URLField(max_length=155, blank=True)
    picture = models.URLField(max_length=155, blank=True)
    saves = models.IntegerField(default=0)