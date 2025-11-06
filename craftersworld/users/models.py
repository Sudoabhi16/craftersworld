from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField


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

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(unique=True, db_index=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["type"]),  # faster filtering by org type
        ]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class User(AbstractUser):
    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("crafter", "Crafter"),
        ("admin", "Admin"),
        ("curator", "Craft Curator"),
        ("support", "Support Agent"),
        ("delivery", "Delivery Partner"),
        ("finance", "Finance Manager"),
        ("marketing", "Marketing"),
        ("moderator", "Moderator"),
        ("partner", "Partner"),
    ]

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
        db_index=True,
    )

    # Option A: single role (simple)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="buyer",
        db_index=True,
    )

    # Option B: multiple roles (Postgres ArrayField)
    roles = ArrayField(
        models.CharField(max_length=20, choices=ROLE_CHOICES),
        default=list,
        blank=True,
        help_text="List of roles assigned to the user",
    )

    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["organisation", "role"]),  # composite index
        ]
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_user_email"),
        ]

    def __str__(self):
        org = self.organisation.name if self.organisation else "No Org"
        role_display = self.get_role_display() if self.role else "No Role"
        return f"{self.username} [{role_display}] @ {org}"
