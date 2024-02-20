from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.utils import timezone


class User(AbstractUser):
    is_verified_email = models.BooleanField(
        default=False, verbose_name=_("Почта подтверждена")
    )
    email = models.EmailField(unique=True, verbose_name=_("Почта"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


def default_expiration():
    return timezone.now() + timezone.timedelta(minutes=5)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="email_verifications"
    )
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=default_expiration)

    def __str__(self) -> str:
        return f"EmailVerification object {self.user.email}"

    def send_verification_email(self):
        verification_link = self.generate_verification_link()
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = f"Для подтверждения учетной записи для {self.user.email} передите по ссылке {verification_link}"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def generate_verification_link(self):
        link = reverse(
            "accounts:verify-email",
            kwargs={"email": self.user.email, "code": self.code},
        )
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        return verification_link

    def is_expired(self):
        return now() >= self.expiration
