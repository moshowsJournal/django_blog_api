from rest_framework import serializers
from django.contrib.auth import login, authenticate, logout
from users.models import User, Token
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model = User
        #Declares required field
        fields = ['username','email','profile_photo','confirm_password','full_name','password']
        extra_kwargs = {
            'password': {'write_only':True}
        }


    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            full_name = self.validated_data['full_name']
        )
        if self.validated_data['password'] != self.validated_data['confirm_password']:
            raise serializers.ValidationError({'status': False,'message':'Passwords do not match'})
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    

    # Ignore these fields if they are not included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self,data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email,password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return user

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = "__all__"




