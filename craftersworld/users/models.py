from django.contrib.auth.models import AbstractUser
from django.db import models


class Organisation(models.Model):
    ORG_TYPE_CHOICES = [
        ("hotel", "Hotel"),
        ("restaurant", "Restaurant"),
        ("bar", "Bar"),
        ("firm", "Firm"),
        ("cafe", "Café"),
        ("spa", "Spa / Wellness"),
        ("venue", "Event Venue"),
        ("office", "Corporate / Office"),
        ("gallery", "Art Gallery"),
    ]

    name = models.CharField(unique=True, db_index=True, max_length=255)
    type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(unique=True, db_index=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class User(AbstractUser):
    ROLE_CHOICES = [
        ("buyer", "Buyer"),     # purchases crafts for organisation use
        ("crafter", "Crafter"), # lists handmade crafts
        ("admin", "Admin"),     # manages organisation account
    ]

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="buyer")

    def __str__(self):
        org = self.organisation.name if self.organisation else "No Org"
        return f"{self.username} [{self.role}] @ {org}"
