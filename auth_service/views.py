from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer
from datetime import datetime, timedelta
from django.core.mail import send_mail


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    # indica alla vista CustomTokenObtainPairView quale serializer deve essere utilizzato per elaborare i dati ricevuti nella richiesta HTTP.
    # Quando una richiesta arriva a CustomTokenObtainPairView, la vista chiama automaticamente il serializer specificato in serializer_class per elaborare i dati.
    serializer_class = CustomTokenObtainPairSerializer

class VerifyEmailView(APIView):
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('code')

        try:
            user = CustomUser.objects.get(username=username)

            # Controlla il codice di verifica
            if user.verification_code != code:
                return Response({"error": "Codice di verifica non valido."}, status=status.HTTP_400_BAD_REQUEST)

            # Controlla se il codice è scaduto
            if user.verification_code_expires_at < datetime.now():
                return Response({"error": "Codice di verifica scaduto."}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica completata
            user.is_active = True
            user.is_verified = True
            user.verification_code = None  # Rimuove il codice
            user.verification_code_expires_at = None  # Rimuove la scadenza
            user.save()

            return Response({"message": "Account verificato con successo."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "Utente non trovato."}, status=status.HTTP_404_NOT_FOUND)

class ResendVerificationCodeView(APIView):
    def post(self, request):
        username = request.data.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            if user.is_verified:
                return Response({"error": "L'account è già verificato."}, status=status.HTTP_400_BAD_REQUEST)
            # Genera un nuovo codice e aggiorna la scadenza
            verification_code = str(random.randint(100000, 999999))
            expiration_time = datetime.now() + timedelta(minutes=10)
            user.verification_code = verification_code
            user.verification_code_expires_at = expiration_time
            user.save()

            # Invia l'email con il nuovo codice
            send_mail(
                'Nuovo Codice di verifica',
                f'Il tuo nuovo codice di verifica è: {
                    verification_code}. Scade in 10 minuti.',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "Codice di verifica inviato nuovamente."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "Utente non trovato."}, status=status.HTTP_404_NOT_FOUND)
