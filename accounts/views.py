from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .models import EmailVerification
from drf_yasg.utils import swagger_auto_schema


class UserRegistrationView(APIView):
    """
    Не стал писать LoginView и делать проверку на user.is_verified_email чтоб не усложнять вход
    """
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email_verification = (
                user.email_verifications.last()
            )  # Get the most recent EmailVerification object
            email_verification.send_verification_email()
            return Response(
                {
                    "message": "Проверьте почту и передите по указанной ссылке для подтверждения"
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, email, code):
        try:
            email_verification = EmailVerification.objects.get(
                user__email=email, code=code
            )
            if email_verification.is_expired():
                return Response(
                    {"message": "Ссылка устарела"}, status=status.HTTP_400_BAD_REQUEST
                )
            email_verification.user.is_verified_email = True
            email_verification.user.save()
            return Response(
                {"message": "Почта успешно подтверждена"}, status=status.HTTP_200_OK
            )
        except EmailVerification.DoesNotExist:
            return Response(
                {"message": "Ссылка недействительна"},
                status=status.HTTP_400_BAD_REQUEST,
            )
