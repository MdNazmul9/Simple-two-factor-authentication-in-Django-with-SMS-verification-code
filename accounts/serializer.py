from django.contrib.auth.password_validation import validate_password
from django.db.models import fields
from rest_framework import serializers
# from .models import User 
from django.contrib.auth import get_user_model
# from rest_framework.authtoken.models import Token
# from employees.models import Designation
from django.contrib.auth.models import Group 

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'user_name')


class EmptySerializer(serializers.Serializer):
    pass


class EmployeeSerializer(serializers.ModelSerializer):
    # code = serializers.CharField(max_length=250)
    # fathers_name =serializers.CharField(max_length=100)
    # mothers_name =serializers.CharField(max_length=100)
    # nid =serializers.CharField(max_length=20)
    # blood_group =serializers.CharField(max_length=20)
    # present_address =serializers.CharField(max_length=500)
    # permanent_address =serializers.CharField(max_length=500)
    # designation_id =serializers.CharField(max_length=100)
    # # gross_salary =serializers.FloatField()

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'user_name', 'contact_no','password', 'password2','user_type', 'status', 'is_editable')
        # exclude = ('is_superuser','groups', 'is_staff', 'is_moderator', 'is_owner', 'is_employee', 'last_login', 'is_active',
            # 'user_permissions')
        ref_name = "User 2"


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password field did not match.'})
        return attrs

    def create(self, validated_data):
        user_name = self.validated_data.get('user_name')
        email = self.validated_data.get('email')
        contact_no = self.validated_data.get('contact_no')
        user_type = self.validated_data.get('user_type')
        status = self.validated_data.get('status')
        is_editable = self.validated_data.get('is_editable')


        user = User.objects.create(user_name=user_name, email=email, contact_no=contact_no,
                    user_type=user_type, status=status, is_editable= is_editable)
        user.set_password(validated_data['password'])

        # user.is_employee= True


        group = Group.objects.get(name='employee')
        user.groups.add(group)

        user.created_by = str(self.context['request'].user)
        user.save()
        return user


class ModeratorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'user_name',  'contact_no','password', 'password2','user_type', 'status', 'is_editable')
        # exclude = ('is_superuser','groups', 'is_staff', 'is_moderator', 'is_owner', 'is_employee', 'last_login', 'is_active',
            # 'user_permissions')


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password field did not match.'})
        return attrs

    def create(self, validated_data):
        user_name = self.validated_data.get('user_name')
        email = self.validated_data.get('email')
        # created_by = self.validated_data.get('created_by')
        contact_no = self.validated_data.get('contact_no')
        user_type = self.validated_data.get('user_type')
        status = self.validated_data.get('status')
        is_editable = self.validated_data.get('is_editable')


        user = User.objects.create(user_name=user_name, email=email, contact_no=contact_no,
                    user_type=user_type, status=status, is_editable= is_editable)
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.is_moderator= True
        group = Group.objects.get(name='moderator')
        user.groups.add(group)
        user.created_by = str(self.context['request'].user)
        user.save()
        return user

class OwnerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'user_name', 'contact_no','password', 'password2','user_type', 'status', 'is_editable')
        # exclude = ('is_superuser','groups', 'is_staff', 'is_moderator', 'is_owner', 'is_employee', 'last_login', 'is_active',
            # 'user_permissions')


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password field did not match.'})
        return attrs

    def create(self, validated_data):
        user_name = self.validated_data.get('user_name')
        email = self.validated_data.get('email')
        # created_by = self.validated_data.get('created_by')
        contact_no = self.validated_data.get('contact_no')
        user_type = self.validated_data.get('user_type')
        status = self.validated_data.get('status')
        is_editable = self.validated_data.get('is_editable')


        user = User.objects.create(user_name=user_name, email=email, contact_no=contact_no,
                    user_type=user_type, status=status, is_editable= is_editable)

        user.set_password(validated_data['password'])
        # user.is_owner = True
        group = Group.objects.get(name='owner')
        user.groups.add(group)
        user.created_by = str(self.context['request'].user)
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'user_name', 'contact_no','password', 'password2','user_type', 'status', 'is_editable')
        # exclude = ('is_superuser','groups', 'is_staff', 'is_moderator', 'is_owner', 'is_employee', 'last_login', 'is_active',
            # 'user_permissions')
        ref_name = 'User 2'


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password field did not match.'})
        return attrs

    def create(self, validated_data):
        user_name = self.validated_data.get('user_name')
        email = self.validated_data.get('email')
        # created_by = self.validated_data.get('created_by')
        contact_no = self.validated_data.get('contact_no')
        user_type = self.validated_data.get('user_type')
        status = self.validated_data.get('status')
        is_editable = self.validated_data.get('is_editable')


        user = User.objects.create(user_name=user_name, email=email, contact_no=contact_no,
                    user_type=user_type, status=status, is_editable= is_editable)

        user.set_password(validated_data['password'])

        group = Group.objects.get(name='customer')
        print(group)
        user.groups.add(group)
        user.created_by = str(self.context['request'].user)
        print(user.created_by)
        user.save()
        return user


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_superuser', 'groups', 'is_staff', 'is_moderator', 'is_owner', 'is_employee', 'last_login', 'is_active',
            'user_permissions')


class ModeratorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_superuser','password', 'groups', 'is_staff', 'is_moderator', 'is_owner', 'is_employee', 'last_login', 'is_active',
            'user_permissions')


class OwnerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','is_superuser', 'groups', 'is_staff', 'is_moderator', 'is_owner', 'is_employee', 'last_login', 'is_active',
            'user_permissions')


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','is_superuser', 'groups', 'is_staff', 'is_moderator', 'is_owner', 'is_employee', 'last_login', 'is_active',
            'user_permissions')


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password field did not match.'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': 'Old password is not correct'})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = '__all__'

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error': 'Please enter valid credentials'})


