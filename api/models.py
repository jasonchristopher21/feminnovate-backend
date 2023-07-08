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

# Create your models here.
class BaseModel(models.Model):
    """
    Base model to be used for all models (except User)
    """
    ceated_at = models.DateTimeField(auto_now_add=True)
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
    
    # TODO: Add experiences, jobs and workshops once the models are created.
    # Should have been depicted as either a one-to-many or many-to-many field.
    saved_jobs = models.ManyToManyField('Job', blank=True)

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
    is_active = models.BooleanField(default=True)
    website = models.URLField(max_length=155, blank=True)