from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField,SerializerMethodField,ValidationError,EmailField,CharField


#django modules
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
        ]

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    confirm_email = EmailField(label='Confirm Email Address')
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'confirm_email',
            'password'

        ]
        extra_kwargs = {'password':{'write_only':True}}


    def validate_email(self, value):
        data = self.get_initial()
        email1 = value
        email2 = data.get('confirm_email')
        if email1 != email2:
            raise ValidationError('Emails must match.')

        if User.objects.filter(email=email2).exists():
            raise ValidationError('This email has been already registered.')
        return value

    def validate_confirm_email(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email2 != email1:
            raise ValidationError('Emails must match.')
        return value

    def create(self, validated_data):
        print(validated_data)
        username    = validated_data.get('username')
        first_name  = validated_data.get('first_name')
        last_name   = validated_data.get('last_name')
        password    = validated_data.get('password')
        email       = validated_data.get('email')
        user_obj = User(username=username,first_name=first_name,last_name=last_name,email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True,read_only=True)
    username = CharField(allow_blank=True,required=False)
    email = EmailField(label='Email Address',allow_blank=True,required=False)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        user_obj = None
        username = attrs.get('username',None)
        email = attrs.get('email',None)
        password = attrs.get('password')
        if not email and not username:
            raise ValidationError('Username or Email is required.')
        user = User.objects.filter(
            Q(email__iexact=email) |
            Q(username__iexact=username)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('Username/Email is not valid')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect Credentials.Please try again.")
        attrs['token'] = 'some random token'
        return attrs

