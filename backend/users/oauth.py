from __future__ import unicode_literals

import logging

from django.contrib.auth.models import User

from oauthlib.common import Request
from oauthlib.oauth2.rfc6749.endpoints.token import TokenEndpoint
from oauthlib.oauth2.rfc6749.tokens import BearerToken
from oauthlib.oauth2.rfc6749.endpoints.base import catch_errors_and_unavailability
from oauthlib.oauth2.rfc6749 import errors
from oauthlib.oauth2.rfc6749.grant_types.refresh_token import RefreshTokenGrant

from .oauth_providers import *

logger = logging.getLogger('django')

providers_associations = {
    'google-oauth2': GoogleOAuth2
}

def get_user_by_access_token(token, provider, nonce):
    """
    Function responsible to retrieve a user given its access_token
    and relative provider
    """
    provider_class = providers_associations.get(provider)
    if provider_class is None:
        raise Exception("Provider not supported")

    return provider_class(token, nonce).get_user()


class SocialTokenGrant(RefreshTokenGrant):

    """`Refresh token grant`_
    .. _`Refresh token grant`: http://tools.ietf.org/html/rfc6749#section-6
    """

    def validate_token_request(self, request):
        # We need to set these at None by default otherwise
        # we are going to get some AttributeError later
        request._params.setdefault("backend", None)
        request._params.setdefault("client_secret", None)

        if request.grant_type != 'convert_token':
            raise errors.UnsupportedGrantTypeError(request=request)

        # We check that a token parameter is present.
        # It should contain the social token to be used with the backend
        if request.token is None:
            raise errors.InvalidRequestError(
                description='Missing token parameter.',
                request=request)

        # We check that a provider parameter is present.
        # It should contain the name of the social provider to be used
        if request.provider is None:
            raise errors.InvalidRequestError(
                description='Missing provider parameter.',
                request=request)

        if not request.client_id:
            raise errors.MissingClientIdError(request=request)

        if not self.request_validator.validate_client_id(request.client_id, request):
            raise errors.InvalidClientIdError(request=request)

        # Existing code to retrieve the application instance from the client id
        if self.request_validator.client_authentication_required(request):
            logger.debug('Authenticating client, %r.', request)
            if not self.request_validator.authenticate_client(request):
                logger.debug('Invalid client (%r), denying access.', request)
                raise errors.InvalidClientError(request=request)
        elif not self.request_validator.authenticate_client_id(request.client_id, request):
            logger.debug('Client authentication failed, %r.', request)
            raise errors.InvalidClientError(request=request)

        # Ensure client is authorized use of this grant type
        # We chose refresh_token as a grant_type
        # as we don't want to modify all the codebase.
        # It is also the most permissive and logical grant for our needs.
        request.grant_type = "refresh_token"
        self.validate_grant_type(request)
        self.validate_scopes(request)

        # TODO: Implement logic to decide whether or not to grant the access_token
        # Decoded body is a list of tuple, dict is better
        body = {}
        for t in request.decoded_body:
            body[t[0]] = t[1]

        user = get_user_by_access_token(token=body['token'], provider=body['provider'], nonce=body['nonce'])
        if user is None:
            raise errors.InvalidClientError("Authentication token for the given provider is invalid")
        request.user = user


class SocialTokenServer(TokenEndpoint):

    """An endpoint used only for token generation."""

    def __init__(self, request_validator, token_generator=None,
                 token_expires_in=None, refresh_token_generator=None, **kwargs):
        """Construct a client credentials grant server.
        :param request_validator: An implementation of
                                  oauthlib.oauth2.RequestValidator.
        :param token_expires_in: An int or a function to generate a token
                                 expiration offset (in seconds) given a
                                 oauthlib.common.Request object.
        :param token_generator: A function to generate a token from a request.
        :param refresh_token_generator: A function to generate a token from a
                                        request for the refresh token.
        :param kwargs: Extra parameters to pass to authorization-,
                       token-, resource-, and revocation-endpoint constructors.
        """
        refresh_grant = SocialTokenGrant(request_validator)
        bearer = BearerToken(request_validator, token_generator,
                             token_expires_in, refresh_token_generator)
        TokenEndpoint.__init__(self, default_grant_type='convert_token',
                               grant_types={
                                   'convert_token': refresh_grant,
                               },
                               default_token_type=bearer)

    # We override this method just so we can pass the django request object
    @catch_errors_and_unavailability
    def create_token_response(self, uri, http_method='GET', body=None,
                              headers=None, credentials=None):
        """Extract grant_type and route to the designated handler."""
        django_request = headers.pop("Django-request-object", None)
        request = Request(
            uri, http_method=http_method, body=body, headers=headers)
        request.scopes = None
        request.extra_credentials = credentials
        request.django_request = django_request
        grant_type_handler = self.grant_types.get(request.grant_type,
                                                  self.default_grant_type_handler)
        logger.debug('Dispatching grant_type %s request to %r.',
                  request.grant_type, grant_type_handler)
        return grant_type_handler.create_token_response(
            request, self.default_token_type)
