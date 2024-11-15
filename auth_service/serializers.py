from rest_framework import serializers
from django.contrib.auth.models import User


import random
from rest_framework import serializers
from .models import CustomUser
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
     # Questo specifica a quale modello del database è associato il serializer.
        model = CustomUser
        # Questo definisce quali campi del modello User devono essere inclusi nel serializer.
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Creazione dell'utente
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False  # L'utente non è attivo fino alla verifica

        # Genera codice di verifica
        verification_code = str(random.randint(100000, 999999))
        expiration_time = datetime.now() + timedelta(minutes=10)  # Codice valido per 10 minuti
        user.verification_code = verification_code
        user.verification_code_expires_at = expiration_time
        user.save()

        # Invia l'email
        subject = "Verifica il tuo account"
        message = f"Ciao {user.username},\n\nIl tuo codice di verifica è: {verification_code}.\n\nGrazie!"
        send_mail(
            subject,
            message,
            'noreply@example.com',  # Email mittente
            [user.email],          # Email destinatario
            fail_silently=False,
        )

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Controlla se l'utente è verificato
        if not self.user.is_verified:
            raise AuthenticationFailed('Utente non verificato. Completa la verifica email.')
        return data