from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/verify/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('register/verify/resend', views.ResendVerificationCodeView.as_view(),
         name='resend-verify-email'),
    path('login/', views.CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),


    # TODO: implementare il logout invalidando il token (blacklist)
]
