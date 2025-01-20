from django.urls import path

from auth_service.views import CallbackView, LoginView, LogoutView, UserProfileView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("callback/", CallbackView.as_view(), name="callback"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserProfileView.as_view(), name="user_profile"),
]