import json
import logging
import requests

import httplib2
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string

from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import detail_route, api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from oauthlib.oauth2.rfc6749.endpoints.token import TokenEndpoint
from oauth2_provider.oauth2_backends import OAuthLibCore
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin

from .oauth import SocialTokenServer, SocialTokenGrant
from .permissions import IsSelfUser
from .serializers import UserSerializer, VoteNotificationSerializer
from .models import Profile, ProfileOAuth2, VoteNotification
from api.serializers import AnalysisTransactionSerializer
from api.models import AnalysisTransaction

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

from django.core.files.storage import default_storage, get_storage_class
from django.core.files.base import ContentFile
from django.conf import settings

import requests
import hashlib
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


logger = logging.getLogger('django')

# TODO: Removed, need to do this better
#create Logger
# user_creation_logger = logging.getLogger('user_creation_logger')
# user_creation_logger.setLevel(logging.DEBUG)
# user_creation_logger_handler = logging.FileHandler("user_creation_logger.log")
# user_creation_logger_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s'))
# user_creation_logger.addHandler(user_creation_logger_handler)

#login logger
# login_logger = logging.getLogger('login_logger')
# login_logger.setLevel(logging.DEBUG)
# login_logger_handler = logging.FileHandler("login_logger.log")
# login_logger_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s'))
# login_logger.addHandler(login_logger_handler)

class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
    ):
    """
    View responsible for the CRUD of the users
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # TODO: This is needed because the creation must not have permisions
    # consider if using another way
    permission_classes = tuple()
    parser_classes = (FormParser, MultiPartParser)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+' # This allows to match against email addresses 

    def create(self, req, *args, **kwargs):
        res = super().create(req, *args, **kwargs)
        if res.status_code == 201:
            user = User.objects.filter(username=res.data['email']).first()
            # FIXME: send_verification_token_email fails on user registration
            user.profile.send_verification_token_email(req)
        return res

    @detail_route(methods=['get'], url_path='notifications', permission_classes=[IsAuthenticated,IsSelfUser])
    def notifications(self, req, username):
        vote_notifications = VoteNotification.objects.filter(user=req.user).order_by('-creation_date').all()[:10]
        res = VoteNotificationSerializer(vote_notifications, many=True).data
        return Response(res, status=HTTP_200_OK)
        
    @detail_route(methods=['get'], permission_classes=[], url_path='image')
    def profile_image(self, request, username):
        user = self.get_queryset().filter(username=username).first()
        return Response(user.profile.profile_image, status=HTTP_200_OK)

    @detail_route(methods=['post'], permission_classes=[IsSelfUser], url_path='change-password')
    def change_password(self, request, username):
        user = self.get_queryset().filter(username=username).first()
        self.check_object_permissions(self.request, user)
        return HttpResponse("Changin password ...")

    @detail_route(methods=['get'], permission_classes=[], url_path='verify')
    def verify_user(self, req, username):
        t = req.GET.get('t', None)
        if t is None:
            return Response('Token should be specified', status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if user is None:
            return Response('Something went wrong, ask again for a verification email')
        # TODO: Check that the token is still valid
        if user.profile.email_verification_token == t:
            user.profile.is_verified = True
            user.save()
            return Response('You\'ve successfully verified your user')
        return Response('Your email confirmation may be expired, go ask a new one', status=HTTP_412_PRECONDITION_FAILED)
    
    @detail_route(methods=['post'], permission_classes=[IsSelfUser], url_path='modify-profile')
    def modify_profile(self,req, username):
        user = self.get_queryset().filter(username=username).first()
        user_serializer = UserSerializer(user, data=req.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response('', status=HTTP_204_NO_CONTENT)
        res = {'error': True, 'res':'user not modified'}
        return Response(res, status=HTTP_400_BAD_REQUEST)
    
    @detail_route(methods=['post'], permission_classes=[IsSelfUser], url_path='change-profile-image')
    def change_profile_image(self, req, username):
        user = req.user
        img = req.data.get("img",None)
        if img is None:
            res = {'error': True, 'res': 'img missing'}
            return Response(res, status=HTTP_400_BAD_REQUEST)
        user.profile.profile_image = img
        user.save()
        res = {'error': False, 'res': '{}{}/{}'.format(
                                                settings.GS_ROOT,
                                                settings.GS_BUCKET_NAME,
                                                user.profile.profile_image.name
                                                )}
        return Response(res, status=HTTP_200_OK)
    

"""
Endpoints for password reset functionalities
"""
class ForgotPassword(APIView):
    def post(self, req):
        pass

class ResetPassword(APIView):
    def post(self, req):
        password = req.data.get('password', None)
        if password is None:
            res = {'error': True,
                    'res': 'password and password check must not be empty'}
            return Response(res, status=HTTP_400_BAD_REQUEST)

        email = req.data.get('email', None)
        user = User.objects.filter(email=email).first()
        if user is None:
            res = {'error': True, 'res': 'email is not correct'}
            return Response(res, status=HTTP_400_BAD_REQUEST)
        if user.profile.reset_email_token != reset_token and user.profile.is_valid_password_reset_token():
            res = {
                'error': True, 'res': 'An error occurred, ask again for a password reset email'}
            return Response(res, status=HTTP_412_PRECONDITION_FAILED)

        user.set_password(password)
        user.save()
        res = {'error': False, 'res': 'Password successfully updated'}
        return Response(res, status=HTTP_200_OK)

class ValidateTokenView(APIView):
    def head(self, req):
        return Response('', status=HTTP_204_NO_CONTENT)

class TransactionState(APIView):
    # TODO: Add the IsSelf permission
    permission_classes = (IsAuthenticated, IsSelfUser, )

    def get(self, req):
        # TODO: Page the results
        transactions = AnalysisTransaction.objects.filter(user=req.user).all()
        transactions_serializer = AnalysisTransactionSerializer(transactions, many=True)
        return Response(transactions_serializer.data, status=HTTP_200_OK)

# OAuth2

class ConvertTokenView(OAuthLibMixin, APIView):
    """
    Endpoint responsible for the conversion of a provider token into an access token
    """
    server_class = SocialTokenServer
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = OAuthLibCore
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
        for key, value in request.data.items():
            request._request.POST[key] = value

        _, headers, body, status = self.create_token_response(request._request)
        response = Response(data=json.loads(body), status=status)

        for k, v in headers.items():
            response[k] = v
        
        return response


class GoogleOauthView(APIView):
    
    permission_classes = (AllowAny,)

    def get(self,request):    
        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        state = get_random_string(64) 
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            os.environ['GOOGLE_CLIENT_SECRET'],
            scopes=['https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile'])
        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required.
        # TODO: This should be dynamic
        flow.redirect_uri = 'https://carbonaraproject.com/users/oauth-redirect'
        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
            state=state)
        return HttpResponseRedirect(authorization_url)

class OauthRedirectView(APIView):

    permission_classes = (AllowAny,)

    def get(self,request):
        
        state = request.query_params.get("state")
        code = request.query_params.get("code")
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                os.environ['GOOGLE_CLIENT_SECRET'],
                scopes=['https://www.googleapis.com/auth/userinfo.email',
                        'https://www.googleapis.com/auth/userinfo.profile'],
                state=state
                )
        flow.redirect_uri = 'https://carbonaraproject.com/users/oauth-redirect'
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        
        credentials = flow.credentials
        token = credentials.token
        service = build('plus', 'v1', credentials=credentials)
        people_resource = service.people()
        people_document = people_resource.get(userId='me').execute()
        emails = people_document['emails']
        email = emails[0]['value']
        first_name = people_document["name"]['givenName']
        last_name = people_document["name"]['familyName']
        img = people_document["image"]["url"]
        img = img.replace('sz=50','sz=500')     
        
        if(User.objects.filter(email=email).first() is None):
            user = User.objects.create_user(email,email,first_name=first_name,last_name=last_name)
            #user.profile.send_verification_token_email(req) fix function parameter
        nonce = get_random_string(64)
        user = User.objects.filter(email=email).first()
        #check if user already has an img
        if(user.profile.profile_image.name.endswith('default-profile-image.png')):
            #email md5 to save profile_image
            hasher = hashlib.md5()
            hasher.update(email.encode('utf-8'))
            email_md5 = hasher.hexdigest()
            img_data = requests.get(img).content 
            image = InMemoryUploadedFile(BytesIO(img_data),None, email_md5+'.jpg', 'image/jpeg',None,None)
            user.profile.profile_image = image
        user.save()
        ProfileOAuth2.objects.create(
            user=user, #TODO: Should be taken from email
            access_token=token,
            nonce=nonce
        )
        data = {
            'client_id': os.environ['CLIENT_ID'], 
            'grant_type': 'convert_token',
            'token': token,
            'provider': 'google-oauth2',
            'nonce': nonce
        }
        res = requests.post('https://carbonaraproject.com' + reverse('convert-token'), data=data)
        print(res)
        logger.error(res.json())
        if res.status_code != HTTP_200_OK:
            # TODO: Redirect user to homepage
            return Response('Something went wrong')
        res_data = res.json()
        res_data['username'] = user.username
        # FIXME: Address should be changed
        return HttpResponseRedirect('https://carbonaraproject.com/#/oauth?access_token={}&username={}'.format(
                                            res_data['access_token'],
                                            res_data['username']
                                        )
                                    )
