from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth import get_user_model, login



      
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        # Hash the password before saving the user
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # Check for duplicate email error
        if 'email' in serializer.errors and 'unique' in serializer.errors['email'][0]:
            return Response({'error': 'Email address is already registered'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if email is None or password is None:
            return Response(
                {"error": "Please provide both email and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, email=email, password=password)
        print("Authenticated user:", user)

        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        user.last_login = timezone.now()
        print(user.last_login)
        user.save()

        login(request, user)

        # serialized_user = CustomUserSerializer(user)

        refresh = RefreshToken.for_user(user)

        print(f"User '{user.email}' successfully logged in!")

        data = {
            "message": "Login successful",
            "token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
        return Response(data, status=status.HTTP_200_OK)