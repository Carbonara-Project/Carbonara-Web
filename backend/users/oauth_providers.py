import requests
import logging
from django.conf import settings
from django.contrib.auth.models import User
from oauthlib.oauth2.rfc6749 import errors

from .models import ProfileOAuth2

logger = logging.getLogger('django')

class BaseProvider():
    """
    Base class for a provider of OAuth2
    """

    def __init__(self, token, nonce):
        self.token = token
        self.nonce = nonce

    def get_email(self):
        pass

    def get_user(self):
        email = self.get_email()
        if email is None:
            logger.error('Could not retrieve email')
            return None
        
        # Get user by email related to the access_token
        user = User.objects.filter(email=email).first()
        if user is None:
            logger.error('No user with that email')
            return None

        profile_oauth2 = ProfileOAuth2.objects.filter(access_token=self.token, nonce=self.nonce).first()
        if profile_oauth2 is None:
            logger.error('Missing ProfileOAuth2 entry')
            return None
        # Check if the access_token is truly related to the email retrived
        if profile_oauth2.user.id != user.id:
            logger.error('User id different from the one in ProfileOAuth2')
            return None
        return user

class GoogleOAuth2(BaseProvider):
    USER_PROFILE_URL = 'https://www.googleapis.com/plus/v1/people/me'

    def get_email(self):
        params = {
            'fields': 'emails/value',
            'key': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        }
        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        res = requests.get(GoogleOAuth2.USER_PROFILE_URL, headers=headers, params=params)
        if res.status_code != 200:
            return None
        # Get first email returned by Google
        return res.json()['emails'][0]['value']