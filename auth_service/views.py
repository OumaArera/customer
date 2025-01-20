from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authlib.integrations.django_client import OAuth # type: ignore
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.conf import settings



# OAuth configuration
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

# Views
class LoginView(APIView):
    def get(self, request):
        return oauth.auth0.authorize_redirect(
            request, request.build_absolute_uri(reverse("callback"))
        )

class CallbackView(APIView):
    def get(self, request):
        token = oauth.auth0.authorize_access_token(request)
        request.session["user"] = token
        return redirect(reverse("user_profile"))

class LogoutView(APIView):
    def get(self, request):
        request.session.clear()
        return redirect(
            f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
            + urlencode(
                {
                    "returnTo": settings.LOGOUT_URL,
                    "client_id": settings.AUTH0_CLIENT_ID,
                },
                quote_via=quote_plus,
            ),
        )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user": request.session.get("user"),
        })
