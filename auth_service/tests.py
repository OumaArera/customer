import json
from unittest.mock import patch, MagicMock
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    @patch("auth_service.views.oauth.auth0.authorize_redirect")
    def test_login_redirect(self, mock_authorize_redirect):
        mock_authorize_redirect.return_value = HttpResponseRedirect("/callback/")
        response = self.client.get(reverse("login"))
        # print("Redirected URL:", response.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/callback/", response.url) 

    @patch("auth_service.views.oauth.auth0.authorize_access_token")
    def test_callback(self, mock_authorize_access_token):
        mock_authorize_access_token.return_value = {
            "access_token": "mock_access_token",
            "id_token": "mock_id_token",
            "userinfo": {"name": "John Doe", "email": "johndoe@example.com"},
        }
        session = self.client.session
        session["user"] = mock_authorize_access_token.return_value
        session.save()

        response = self.client.get(reverse("callback"))
        # print("Redirected URL:", response.url)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(
            self.client.session["user"], mock_authorize_access_token.return_value
        )

    def test_user_profile(self):
        user = {"name": "John Doe", "email": "johndoe@example.com"}
        session = self.client.session
        session["user"] = user
        session.save()

        with patch("rest_framework.views.APIView.get_permissions") as mock_permissions:
            mock_permissions.return_value = [MagicMock()]
            response = self.client.get(reverse("user_profile"))
            # print("Response Data:", json.dumps(response.data, indent=2))

        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["email"], "johndoe@example.com")
