from django.urls import path, include
from .views import SignUpView
from .views import SignUpView, CustomLoginView, ChangePasswordView, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "login/",
        CustomLoginView.as_view(
            redirect_authenticated_user=True, template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path("profile/", profile, name="users-profile"),
    path("password_change/", ChangePasswordView.as_view(), name="password_change"),
]
