from rest_framework import serializers,exceptions
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from .serializers import SignupSerializer,PasswordChangeSerializer,LoginSerializer,ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import redirect,render
from rest_framework import status
from django.utils.encoding import force_text
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from authentication.tokens import account_activation_token
from utils import emailing
import random
import string
from rest_framework.exceptions import NotFound,APIException
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView
)

UserModel = get_user_model()

class SignupAPIView(APIView):
    permission_classes=(AllowAny,)
    def validate_password(self,value):
        if(len(value)<getattr(settings,'PASSWORD_MIN_LENGTH',8)):
             raise serializers.ValidationError('Password should be at least %s characters long' % getattr(settings,'PASSWORD_MIN_LENGTH',8))
        return value

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):#below statement will be executed if serializers data is valid otherwise it will raise exceptions
            email=serializer.validated_data['email']
            phone=serializer.validated_data['phone']
            user_type = serializer.validated_data['user_type']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            password = serializer.validated_data['password']
            user = UserModel.objects.create(first_name=first_name, last_name=last_name, email=email,phone=phone, user_type=user_type,is_active=False)
            try:
                self.validate_password(password)
            except ValidationError as error:
                 raise exceptions.ValidationError(error)
            user.set_password(password)
            user.save()
            #sending mail to user mail account
            context={
                'user':user,
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            }
            mail_subject='Activate your Accout'
            message= render_to_string('verification.html',context)
            email_plaintext_message= render_to_string('verification.txt',context)
            to_email=email
            success= emailing.EmailThread(mail_subject,message,context,[email,]).start()
            return Response({'data':serializer.data,'success':'User registered sucessfully'},status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=UserModel.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,UserModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        return render(request,"msg.html",context={'user_type':user.user_type})
    else:
        return HTTPResponse('Activation link is invalid')
    
    # login_view
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return{
    'refresh':str(refresh),
    'access':str(refresh.access_token)
    }
class LoginAPIView(APIView):
    def  authenticate(self, request,email,password,*args, **kwargs):
        UserModel = get_user_model()#users.models.PortalUser
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise NotFound({'detail':'User not found'})
        else:
            if user.is_active :
                if user.check_password(password):
                    return user
            else:
                raise APIException({'detail':'user not verified'})
        raise NotFound({'detail':'User with proper credentials does not exist'})
    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user_obj = self.authenticate(request,email,password)#returns email address of user input
            if user_obj:
                token = get_tokens_for_user(user_obj)
                token['user_type'] = user_obj.user_type
                token['username'] = user_obj.email
                return Response(token)
            else:
                return Response({'detail':'Active user not found.'})
class PasswordChangeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def get_object(self,queryset=None):
        obj = self.request.user
        return obj    
    def post(self,request):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not self.object.check_password(serializer.data.get("old_password")):
                raise APIException("you entered wrong password")
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"data":"Password Change Success"},status=status.HTTP_200_OK)

class UserProfileAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer #authentication.api.serializer.ProfileSerializer
    def get(self,request):
        user_obj = UserModel.objects.get(id=request.user.id)
        user_data = self.serializer_class(user_obj).data
        return Response(data=user_data,status=status.HTTP_200_OK)

class UserProfileUpdateAPIView(UpdateAPIView):
     permission_classes = (IsAuthenticated,)
     queryset = UserModel.objects.all()
     serializer_class = ProfileSerializer
     def patch(self, request, *args, **kwargs):
         user_obj = self.kwargs['pk']
         if request.user.id == user_obj:
             return self.partial_update(request,*args,**kwargs)
         return Response({'detail': 'you donot have permission to update the profile'},
                        status=status.HTTP_400_BAD_REQUEST)

# class ForgetPasswordView(APIView):
#     def authenticate(self,request,email):
#         UserModel=get_user_model()
#         try:
#             user=UserModel.objects.get(email=email)
#         except UserModel.DoesNotExist:
#             raise NotFound({'detail':'User not found'})
#         else:
#             if user.is_active:
#                 return user
#             else:
#                 raise APIException({'detail':'user is not verified'})

#     def randomStringwithDigitsAndSymbols(self,stringLength=8):
#         password_characters = string.ascii_letters + string.digits + string.punctuation
#         for i in range(stringLength):
#             return ''.join(random.choice(password_characters))

#     def post(self,request,*args,**kwargs):
#         UserModel=get_user_model()
#         serializer=PasswordResetSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email=serializer.validated_data.get('email')
#             user_obj = self.authenticate(request,email)
#             if user_obj:
#                 a= randomStringwithDigitsAndSymbols()
#                 password=user_obj.password
#                 password.delete()
#                 UserModel.objects.set_password(a)

# class PasswordResetAPIVIew(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = PasswordResetSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.validated_data['email']
#             user_type = serializer.validated_data['user_type']
#             try:
#                 user = UserModel.objects.get(email=email, user_type=user_type)
#                 if user.is_active:
#                     key = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
#                     pwd_reset_obj, new_pwd_reset_obj = UserPasswordReset.objects.get_or_create(key=key, user=user,
#                                                                                                is_active=True)
#                     if pwd_reset_obj:
#                         context = {
#                             'user': user.email,
#                             'token': pwd_reset_obj.key,
#                              'user_type': user_type
#                         }
#                     else:
#                         context = {
#                             'user': user.email,
#                             'token': new_pwd_reset_obj.key,
#                             'user_type': user_type
#                         }
#                     mail_subject = 'Password Reset Request'
#                     message = render_to_string('authentication/password_reset.html', context)
#                     success = emailing.EmailThread(mail_subject, message, context, [user.email, ]).start()
#                     return Response(
#                         {'data': serializer.data, 'success': 'Please check your email and complete the process.'})
#                 else:
#                     raise APIException("User is not activated.")
#             except UserModel.DoesNotExist:
#                 raise NotFound("User with the provided Email does not exist.")

           






            


            




             
         


















