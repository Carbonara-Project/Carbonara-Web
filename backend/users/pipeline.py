from django.contrib.auth.models import User
from social_core.pipeline.partial import partial
from rest_framework.request import QueryDict

def save_user(backend, user, response, *args, **kwargs):
    email = response.get('email', None)
    #email = kwargs['details']['email']
    if email is None:
        email = kwargs['details']['email']      
    if not User.objects.filter(email=email).first():
        User.objects.create_user(username=email, email=email)

@partial
def redirect_token(strategy, backend, response, request, details, *args, **kwargs):
    # If the request is a token-something request, let it pass through
    if 'grant_type' in request:
        return None 
    return strategy.redirect(
        '/#/oauth?' +
        'email=' + details['email'] + 
        '&auth_token=' + response['access_token'] +
        '&backend=' + backend.name
    )
