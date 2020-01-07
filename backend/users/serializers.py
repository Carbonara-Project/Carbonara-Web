from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Profile
from .models import VoteNotification

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    '''
    email is required 
    Username with length_max = 32
    Password is write_only to ensure security
    '''

    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField(allow_blank=True, allow_null=True)
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    bio = serializers.CharField(allow_blank=True, allow_null=True, write_only=True)

    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        # Here we use the email also for the username field
        user = User.objects.create_user(
                                        username=validated_data['email'],
                                        email=validated_data['email'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name']
                                        )
        return user

    def update(self, instance, validated_data):
        instance.profile.bio = validated_data.get('bio', instance.profile.bio)    
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['profile_image'] = '{}{}/{}'.format(
                                                settings.GS_ROOT,
                                                settings.GS_BUCKET_NAME,
                                                instance.profile.profile_image.name
                                                )
        res['bio'] = instance.profile.bio
        return res

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'bio')

class VoteNotificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.CharField()
    by = serializers.CharField()

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['binary_md5'] = instance.procedure_desc.procedure.program.md5
        res['procedure_offset'] = instance.procedure_desc.procedure.offset
        return res

    class Meta:
        model = VoteNotification
        fields = '__all__'
