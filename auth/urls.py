from django.urls import path
from django.conf import settings
from auth.signin.views import AuthSigninView
from auth.signup.views import AuthSignupView
from auth.reset_password.views import AuthResetPasswordView
from auth.new_password.views import AuthNewPasswordView

app_name = 'auth'

urlpatterns = [
    path('signin', AuthSigninView.as_view(template_name = 'pages/auth/signin.html'), name='signin'),
    path('signup', AuthSignupView.as_view(template_name = 'pages/auth/signup.html'), name='signup'),
    path('reset-password', AuthResetPasswordView.as_view(template_name = 'pages/auth/reset-password.html'), name='reset-password'),
    path('new-password', AuthNewPasswordView.as_view(template_name = 'pages/auth/new-password.html'), name='new-password'),
]