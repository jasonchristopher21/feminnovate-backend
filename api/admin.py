from django.contrib import admin

from api.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(Workshop)
admin.site.register(Job)