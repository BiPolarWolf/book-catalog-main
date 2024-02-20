from django.urls import path
from .views import UserRegistrationView, VerifyEmailView

app_name = "accounts"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path(
        "verify-email/<str:email>/<uuid:code>/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),
]
