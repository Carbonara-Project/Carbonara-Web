from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
import oauth2_provider.views as oauth2_views

from .views import UserViewSet, ResetPassword, ForgotPassword, ValidateTokenView, TransactionState, ConvertTokenView, GoogleOauthView, OauthRedirectView

users_router= SimpleRouter()
users_router.register(r'profile', UserViewSet)

urlpatterns = users_router.urls + [
    url(r'^reset-password/$', ResetPassword.as_view(), name='reset_password'),
    url(r'^forgot-password/$', ForgotPassword.as_view(), name='forgot-password'),

    url(r'^validate-token/?$', ValidateTokenView.as_view(), name="access-token"),

    url(r'^transactions/$', TransactionState.as_view(), name='transactions'),

    # OAuth2
    url(r'^o/authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^o/token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^o/revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
    url(r'^o/convert-token/?$', ConvertTokenView.as_view(), name="convert-token"),

    url(r'^google-oauth/$', GoogleOauthView.as_view(), name="google-oauth"),
    url(r'^oauth-redirect/$',OauthRedirectView.as_view(),name="oauth-redirect"),
]