from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rooms.models import CheckInInformation

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'tokens')

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = True
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        print(f"Validating with email: {email}")

        if email and password:
            try:
                user = User.objects.get(email=email)
                print(f"User found: {user}")
                print(f"Password check: {user.check_password(password)}")
                user = authenticate(email=email, password=password)
                print(f"Authenticated user: {user}")
                if not user:
                    raise serializers.ValidationError('Неверные учетные данные')
            except User.DoesNotExist:
                print("User not found")
                raise serializers.ValidationError('Пользователь не найден')
        else:
            raise serializers.ValidationError('Email и пароль обязательны')

        attrs['user'] = user
        return attrs

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': str(refresh.access_token)}
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInInformation
        fields = ('name', 'surname', 'fathername', 'phone_number', 
                 'birth_date', 'university', 'faculty', 'course', 
                 'email', 'check_in_date', 'check_out_date', 'room') 