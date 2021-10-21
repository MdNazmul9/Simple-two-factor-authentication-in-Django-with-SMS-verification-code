from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from django.urls import path

from .api import ChangePasswordView, ResetPasswordView
from .views import (user_logout, home, AuthViewSet,
                    CustomerCreateApi, ModeratorCreateApi, OwnerCreateApi, EmployeeCreateApi,
                    ModeratorListApi, OwnerListApi, CustomerListApi, EmployeeListApi,
                    ModeratorUpdateApi, OwnerUpdateApi, CustomerUpdateApi, EmployeeUpdateApi,
                    ModeratorDeleteApi, OwnerDeleteApi, CustomerDeleteApi, EmployeeDeleteApi,
                    ModeratorDetailsApi, OwnerDetailsApi, CustomerDetailsApi, EmployeeDetailsApi, MyTokenObtainPairView,
                    )

app_name = 'accounts'
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.register('auth', AuthViewSet, basename='auth')

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('home/', home, name='home'),
    path('users/login/', MyTokenObtainPairView.as_view(), name='mytoken_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', user_logout, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),

    # Change password API URL
    path('auth/change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),

    # Reset password API URL
    path('auth/reset_password/', ResetPasswordView.as_view(), name='reset-password'),

    # create api url
    path('customer/create/', CustomerCreateApi.as_view(), name='customer_create_api'),  # api for create Customer user
    path('employee/create/', EmployeeCreateApi.as_view(), name='employee_create_api'),  # api for create Employee user
    path('moderator/create/', ModeratorCreateApi.as_view(), name='moderator_create_api'),
    # api for create moderator user
    path('owner/create/', OwnerCreateApi.as_view(), name='owner_create_api'),  # api for create owner user

    # list api url
    path('customer/list/', CustomerListApi.as_view(), name='customer_list_api'),  # api for list Customer user
    path('employee/list/', EmployeeListApi.as_view(), name='employee_list_api'),  # api for list Employee user
    path('moderator/list/', ModeratorListApi.as_view(), name='moderator_list_api'),  # api for list moderator user
    path('owner/list/', OwnerListApi.as_view(), name='owner_list_api'),  # api for list owner user

    # Details api url
    path('customer/list/<int:pk>/', CustomerDetailsApi.as_view(), name='customer_details_api'),  # api for Details usual user
    path('employee/list/<int:pk>/', EmployeeDetailsApi.as_view(), name='employee_details_api'),
    # api for Details Employee user
    path('moderator/list/<int:pk>/', ModeratorDetailsApi.as_view(), name='moderator_details_api'),
    # api for Details moderator user
    path('owner/list/<int:pk>/', OwnerDetailsApi.as_view(), name='owner_details_api'),  # api for Details owner user

    # update api url
    path('customer/update/<int:pk>/', CustomerUpdateApi.as_view(), name='customer_update_api'),  # api for update Customer user
    path('employee/update/<int:pk>/', EmployeeUpdateApi.as_view(), name='employee_update_api'),
    # api for update Employee user
    path('moderator/update/<int:pk>/', ModeratorUpdateApi.as_view(), name='moderator_update_api'),
    # api for update moderator user
    path('owner/update/<int:pk>/', OwnerUpdateApi.as_view(), name='owner_update_api'),  # api for update owner user

    # delete api url
    path('customer/delete/<int:pk>/', CustomerDeleteApi.as_view(), name='customer_delete_api'),  # api for delete Customer user
    path('employee/delete/<int:pk>/', EmployeeDeleteApi.as_view(), name='employee_delete_api'),
    # api for delete Employee user
    path('moderator/delete/<int:pk>/', ModeratorDeleteApi.as_view(), name='moderator_delete_api'),
    # api for delete moderator user
    path('owner/delete/<int:pk>/', OwnerDeleteApi.as_view(), name='owner_delete_api'),  # api for delete owner user

]
urlpatterns += router.urls
# login api  is = accounts/auth/login/
# Logout api  is = accounts/auth/logout/
