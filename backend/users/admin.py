from django.contrib import admin

from .models import Profile, ProfileOAuth2, VoteNotification

admin.site.register(Profile)
admin.site.register(ProfileOAuth2)
admin.site.register(VoteNotification)
