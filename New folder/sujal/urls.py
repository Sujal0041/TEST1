from django.urls import path
from .views import  register_user, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register_user, name='register'),
]