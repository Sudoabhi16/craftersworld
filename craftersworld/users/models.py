from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    organization_address = models.TextField(blank=True, null=True)
    individual_full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username