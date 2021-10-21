from django.contrib.auth.models import update_last_login
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
# from .forms import UserRegistrationForm
# from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import AuthenticationForm


from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions

# from . import serializer
from rest_framework_simplejwt.settings import api_settings

from .utils import get_and_authenticate_user

from rest_framework import generics
from rest_framework.response import Response
from .serializer import (
    EmptySerializer, 
    UserLoginSerializer, 
    AuthUserSerializer,    
    CustomerSerializer,
    ModeratorSerializer, 
    OwnerSerializer, 
    EmployeeSerializer,
    EmployeeUpdateSerializer,
    ModeratorUpdateSerializer,
    OwnerUpdateSerializer,
    CustomerUpdateSerializer
    )

# from .models import User
# from braces.views import LoginRequiredMixin, StaffuserRequiredMixin, SuperuserRequiredMixin
from django.db.models import Q
from .custome_permissions import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        # token['message'] = 'Hello World!'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.user_name
        data['email'] = self.user.email
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = get_and_authenticate_user(request, **serializers.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)
        # return redirect('accounts/home')

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return redirect('home')

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


def home(request):
    
    return render(request, 'accounts/home.html')


def user_logout(request):
    logout(request)
    return redirect('home')


# api create view for Employee user
class EmployeeCreateApi(generics.CreateAPIView):
    employee_group = models.Group.objects.get(name='employee')
    queryset = employee_group.user_set.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsOwnerOrModerator]


# api create view for moderator user
class ModeratorCreateApi(generics.CreateAPIView):
    moderator_group = models.Group.objects.get(name='moderator')
    queryset = moderator_group.user_set.all()
    serializer_class = ModeratorSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions,  IsAdminUser]


# api create view for owner user
class OwnerCreateApi(generics.CreateAPIView):
    owner_group = models.Group.objects.get(name='owner')
    queryset = owner_group.user_set.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions,  IsModerator]


# api for create  view for Customer user
class CustomerCreateApi(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsEmployeeOrOwnerOrModerator]
    customer_group = models.Group.objects.get(name='customer')
    queryset = customer_group.user_set.all()
    serializer_class = CustomerSerializer


# api for list view for Employee user
class EmployeeListApi(generics.ListAPIView):
    employee_group = models.Group.objects.get(name='employee')
    queryset = employee_group.user_set.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsOwnerOrModerator]


# api for list view for Moderator user
class ModeratorListApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions,  IsSuperUser]
    moderator_group = models.Group.objects.get(name='moderator')
    queryset = moderator_group.user_set.all()
    serializer_class = ModeratorSerializer


# api for list view for Owner user
class OwnerListApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions,  IsModerator]
    owner_group = models.Group.objects.get(name='owner')
    queryset = owner_group.user_set.all()
    serializer_class = OwnerSerializer


# api for list view for Customer user
class CustomerListApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsEmployeeOrOwnerOrModerator]
    customer_group = models.Group.objects.get(name='customer')
    queryset = customer_group.user_set.all()
    serializer_class = CustomerSerializer


# api details for  Employee user
class EmployeeDetailsApi(generics.RetrieveAPIView):
    employee_group = models.Group.objects.get(name='employee')
    queryset = employee_group.user_set.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions,  IsSelfOrOwnerOrModerator]


# api for details moderator user
class ModeratorDetailsApi(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions,  IsSelfOrSuperUser]
    moderator_group = models.Group.objects.get(name='moderator')
    queryset = moderator_group.user_set.all()
    serializer_class = ModeratorSerializer


# api for details owner user
class OwnerDetailsApi(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsSelfOrModerator]
    owner_group = models.Group.objects.get(name='owner')
    queryset = owner_group.user_set.all()
    serializer_class = OwnerSerializer


# api  details for Customer user
class CustomerDetailsApi(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,  DjangoModelPermissions, IsSelfOrEmployeeOrOwnerOrModerator]
    customer_group = models.Group.objects.get(name='customer')
    queryset = customer_group.user_set.all()
    serializer_class = CustomerSerializer


# api for update Employee user
class EmployeeUpdateApi(generics.RetrieveUpdateAPIView):
    employee_group = models.Group.objects.get(name='employee')
    queryset = employee_group.user_set.all()
    serializer_class = EmployeeUpdateSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsOwnerOrModerator, IsEditable]


# api for update moderator user
class ModeratorUpdateApi(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated,   IsSuperUser, IsEditable]
    moderator_group = models.Group.objects.get(name='moderator')
    queryset = moderator_group.user_set.all()
    serializer_class = ModeratorUpdateSerializer


# api for update owner user
class OwnerUpdateApi(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated,  DjangoModelPermissions, IsModerator, IsEditable]
    owner_group = models.Group.objects.get(name='owner')
    queryset = owner_group.user_set.all()
    serializer_class = OwnerUpdateSerializer


# api for update usual user
class CustomerUpdateApi(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated,  DjangoModelPermissions, IsEditable, IsEmployeeOrOwnerOrModerator]
    customer_group = models.Group.objects.get(name='customer')
    queryset = customer_group.user_set.all()
    serializer_class = CustomerUpdateSerializer


# api for delete Employee user
class EmployeeDeleteApi(generics.DestroyAPIView):
    employee_group = models.Group.objects.get(name='employee')
    queryset = employee_group.user_set.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated,  DjangoModelPermissions, IsOwnerOrModerator]


# api for delete moderator user
class ModeratorDeleteApi(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    moderator_group = models.Group.objects.get(name='moderator')
    queryset = moderator_group.user_set.all()
    serializer_class = ModeratorSerializer


# api for delete owner user
class OwnerDeleteApi(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsAdminUser]
    owner_group = models.Group.objects.get(name='owner')
    queryset = owner_group.user_set.all()
    serializer_class = OwnerSerializer


# api for delete usual user
class CustomerDeleteApi(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,  DjangoModelPermissions, IsAdminUser]
    customer_group = models.Group.objects.get(name='customer')
    queryset = customer_group.user_set.all()
    serializer_class = CustomerSerializer

# def register_user(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration successful.")
#             return redirect('login')
#         else:
#             context = {'error': True, 'form': form}
#             return render(request, 'accounts/registration.html', context)
#     else:
#         form = UserRegistrationForm()
#         return render(request, 'accounts/registration.html', {'form': form})


# def login_user(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#     return render(request=request, template_name="accounts/login.html")
