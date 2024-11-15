from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, datetime


class CustomUser(AbstractUser):
    # Indica se l'utente ha verificato l'email
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(
        max_length=6, blank=True, null=True)  # Codice per la verifica
    verification_code_expires_at = models.DateTimeField(
        blank=True, null=True)  # Campo per la scadenza
