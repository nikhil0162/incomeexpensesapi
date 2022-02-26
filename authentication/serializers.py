from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import exceptions
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        Serializer, ValidationError)

from .utils import Util

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    password = CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email','username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise ValidationError('Username must be in alphanumeric characters')
        return attrs

    def create(self, validated_data):
        password_value = validated_data.pop('password', None)
        user_obj = User.objects.create_user(**validated_data)
        user_obj.set_password(password_value)
        user_obj.save()
        return user_obj


class EmailVerificationSerializer(ModelSerializer):
    token = CharField(max_length=555)

    class Meta:
        model = User
        fields= ['token']


class LoginSerializer(ModelSerializer):
    email = EmailField(max_length=255)
    password = CharField(max_length=68, min_length=6, write_only=True)
    tokens = CharField(max_length=500, min_length=6,read_only=True)

    class Meta:
        model = User
        fields= ['email', 'password', 'tokens']

    def validate(self, attrs):        
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user= authenticate(email=email, password=password)

        if not user:
            raise exceptions.AuthenticationFailed("Invalid email or password")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("Account disabled, contact admin")

        if not user.is_verified:
            raise exceptions.AuthenticationFailed("Email is not verified")

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
            }
        return super().validate(attrs)
         

class RequestPasswordResetEmailSerializer(Serializer):
    email = EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):     
        print(self.context['request'])   
        email = attrs.get('email', '')
        if User.objects.filter(email=email).first():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            # get link
            relative_link = reverse('authentication:password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            print(self.context['request'])
            domain = get_current_site(self.context['request']).domain
            absurl = f'http://{domain}{relative_link}'
            
            email_body = f'Hello, \n Use below link to reset your password \n {absurl}'
            data = {
                'email_body': email_body,
                'subject': 'Reset your password',
                'to_email': user.email,
            }
            Util.send_mail(data)
        return super().validate(attrs)


class SetPasswordSerializer(Serializer):
    password = CharField(max_length=68, min_length=6, write_only=True)
    token = CharField(min_length=1, write_only=True)
    uidb64 = CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user_obj = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user_obj, token):
                return exceptions.AuthenticationFailed('The reset link is invalid', 401)
            
            user_obj.set_password(password)
            user_obj.save()
        except DjangoUnicodeDecodeError:
            raise ValidationError('customize Unicode error')
        except User.DoesNotExist:
            raise ValidationError('User Does not exist')
        return super().validate(attrs)
