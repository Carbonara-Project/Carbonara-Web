import datetime
import sendgrid
import os
from sendgrid.helpers.mail import *

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from rest_framework.reverse import reverse
from rest_framework.request import Request
from django.utils import timezone
from django.utils.crypto import get_random_string
#from oauth2client.contrib.django_orm import FlowField, CredentialsField

from api.models import Program, ProcedureDesc

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #profile_image = models.CharField(max_length=256, default='***')
    profile_image = models.ImageField(upload_to='profile_image', default='profile_image/default-profile-image.png')
    bio = models.TextField()

    # Wether or not a user has completed a verification of his account from his email
    is_verified = models.BooleanField(default=False)
    
    email_verification_token = models.CharField(
        max_length=settings.EMAIL_VERIFICATION_TOKEN_LENGTH,
        validators=[MinLengthValidator(settings.EMAIL_VERIFICATION_TOKEN_LENGTH)],
    )
    email_verification_token_creation_date = models.DateTimeField(null=True)
    
    reset_email_token = models.CharField(
        max_length=settings.PASSWORD_RESET_TOKEN_LENGTH,
        validators=[MinLengthValidator(settings.PASSWORD_RESET_TOKEN_LENGTH)],
        null=True,
        blank=True
    )
    reset_email_token_creation_date = models.DateTimeField(null=True, blank=True)

    def send_verification_token_email(self, req: Request):
        email_verification_token = get_random_string(length=32)
        self.email_verification_token = email_verification_token
        self.email_verification_token_creation_date = timezone.now()
        self.save()

        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("test@example.com")
        to_email = Email(self.user.email)
        subject = "Confirm registration"
        content = Content(
            "text/plain",
            "To confirm your account simply go to this link {}?t={}".format(
                                            reverse(
                                                'user-verify',
                                                args=[self.user.username],
                                                request=req
                                            ),
                                            email_verification_token
                                            )
        )
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code not in range(200, 300):
            print(response.status_code)
            print(response.body)
            print(response.headers)

    """
    Method to send a reset_password_token_email to the requested user
    """
    @staticmethod
    def send_password_reset_email(username, req):
        reset_token = get_random_string(length=32)
        self.reset_email_token = reset_token
        self.reset_email_token_creation_date = timezone.now()
        self.save()

        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("test@example.com")
        to_email = Email(self.user.email)
        subject = "Reset password"
        content = Content(
            "text/plain",
            "To reset you password simply go to this link {}?t=".format(
                                            reverse(
                                                'reset_password',
                                                args=[username],
                                                request=req
                                                ),
                                            reset_token
                                            )
        )
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code not in range(200, 300):
            print(response.status_code)
            print(response.body)
            print(response.headers)

    def is_valid_password_reset_token(self):
        VALID_HOURS_SPAN = datetime.delta(hours=settings.EMAIL_VERIFICATION_TOKEN_DURATION)
        now = timezone.now()
        creation_date = self.reset_email_token_creation_date
        hours_delta = (creation_date - now).seconds // 60
        return hours_delta < VALID_HOURS_SPAN
    
    def __str__(self):
        return '<User: {}>'.format(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProfileOAuth2(models.Model):
    """
    Model associating User to an access_token provided by
    an external provider
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=256) # TODO: Check this is sufficient
    nonce = models.CharField(max_length=64)

    creation = models.DateTimeField(default=timezone.now)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.TextField()
    action = models.TextField()

    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class VoteNotification(Notification):
    procedure_desc = models.ForeignKey(ProcedureDesc)
    by = models.ForeignKey(User, related_name='notifications_by_user_set')

# TODO: Decide whether or not to keep this
# class FlowModel(models.Model):
#   id = models.ForeignKey(User, primary_key=True)
#   flow = FlowField()

# class CredentialsModel(models.Model):
#   id = models.ForeignKey(User, primary_key=True)
#   credential = CredentialsField()
