from django.db import models
from django.utils.translation import gettext_lazy as _ 

class JobType(models.TextChoices):
    FULL_TIME = 'Full-time', _('Full Time')
    PART_TIME = 'Part-time', _('Part Time')
    INTERNSHIP = 'Internship', _('Internship')
    FREELANCE = 'Freelance', _('Freelance')
    OTHER = 'Other', _('Other')

class Experience(models.TextChoices):
    LESS_THAN_1 = 'LT1', _('Less than 1 year')
    BETWEEN_1_2 = 'B12', _('Between 1 and 2 years')
    BETWEEN_2_6 = 'B26', _('Between 2 and 6 years')
    GREATER_THAN_6 = 'GT6', _('Greater than 6 years')