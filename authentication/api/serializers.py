from rest_framework import serializers
from django.core import validators
from django.conf import settings
from django.contrib.auth import get_user_model # This method will return the currently active user model
UserModel = get_user_model() 

class SignupSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone =serializers.CharField(max_length=11,validators=[validators.int_list_validator(),validators.MinLengthValidator(10)])
    password = serializers.CharField()
    user_type =serializers.CharField()
    first_name =serializers.CharField()
    last_name = serializers.CharField()

class Meta:
    fileds = ('first_name', 'last_name', 'phone', 'password', 'user_type', 'email')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type':'password'})
    
# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(
                    settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value
    
    def validate(self,data):
        if data.get('old_password')==data.get('new_password'):
            raise serializers.ValidationError({"detail":"You enter the old password"})
        return data
    
    def validate_new_password(self,value):
        self.validate_password(value)
        return value

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
       model = UserModel
       fields = ['id', 'first_name', 'last_name', 'username','email','phone','address', 'image', 'user_type']
       read_only_fields = ['email','user_type']

# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     user_type = serializers.CharField()

       








  

