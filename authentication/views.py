import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .renderers import UserRenderer
from .serializers import (EmailVerificationSerializer, LoginSerializer,
                          RegisterSerializer,
                          RequestPasswordResetEmailSerializer,
                          SetPasswordSerializer)
from .utils import Util

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class= RegisterSerializer

    def post(self,request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # creating token
            user_obj = User.objects.filter(email=serializer.data['email']).first()
            token = RefreshToken.for_user(user_obj).access_token

            # get link
            relative_link = reverse('authentication:verify-email')
            domain = get_current_site(request).domain
            absurl = f'http://{domain}{relative_link}?token={str(token)}'
            
            email_body = f'Hi, {user_obj.username} Use below link to verify your email \n {absurl}'
            data = {
                'email_body': email_body,
                'subject': 'Verify your email',
                'to_email': user_obj.email,
            }
            Util.send_mail(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(views.APIView):
    serializer_classs = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY,description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY, algorithms='HS256')
            print(payload['user_id'])
            user_obj = User.objects.get(id=payload['user_id'])
            if not user_obj.is_verified:
                user_obj.is_verified = True
                user_obj.save()

            return Response({'email': 'Successfully Activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self,request):
        email = request.data.get('email')
        serializer = self.serializer_class(context={'request':request},data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': 'We have sent you a reset password link.'}, status=status.HTTP_200_OK)

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode


class PasswordTokenCheckAPI(generics.GenericAPIView):
    
    def get(self, request,uidb64,token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user_obj = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user_obj, token):
                return Response({'error': 'Token is not valid, request a new one.'})
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user_obj, token):
                return Response({'error': 'Token is not valid, request a new one.'})
        return 


class SetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetPasswordSerializer

    def patch(self,request):
        serializer= self.get_serializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message': 'Password reset success', 'status':status.HTTP_200_OK})

    