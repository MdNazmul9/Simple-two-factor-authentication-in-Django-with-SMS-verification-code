from rest_framework import permissions

from django.contrib.auth import models

moderator_group = models.Group.objects.get(name='moderator')
moderators = moderator_group.user_set.all()


owner_group = models.Group.objects.get(name='owner')
owners = owner_group.user_set.all()


employee_group = models.Group.objects.get(name='employee')
employees = employee_group.user_set.all()



customer_group = models.Group.objects.get(name='customer')
customers = customer_group.user_set.all()

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False



class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user in moderators or request.user.is_staff:
            return True
        return False




class IsOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user in moderators or request.user in owners:
            return True
        return False

   

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if  request.user in owners:
            return True
        return False




class IsEmployeeOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if  request.user in owners or request.user in employees:
            return True
        return False

    


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if  request.user in employees:
            return True
        return False

   

class IsEmployeeOrOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user in employees or request.user in owners:
            return True
        return False


class IsSelfOrEmployeeOrOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active or request.user.is_staff or request.user in employees or request.user in owners
        
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff or request.user in employees or request.user in owners
    


class IsSelfOrOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active or request.user.is_staff or request.user in owners
        
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff or request.user in owners


class IsSelfOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active or request.user in moderators or request.user.is_superuser
        
    def has_object_permission(self, request, view, obj):
        return obj != None and ( obj == request.user or request.user in moderators or request.user.is_superuser)




class IsSelfOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active or request.user.is_superuser
        
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser


class IsEditable(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active 
        
    def has_object_permission(self, request, view, obj):
        return obj.is_editable ==True 

class ActualDjangoModelPermissions(permissions.DjangoModelPermissions):
    view_permissions = ['%(app_label)s.view_%(model_name)s']

    perms_map = {
        'GET': view_permissions,
        'OPTIONS': view_permissions,
        'HEAD': view_permissions,
        'POST': permissions.DjangoModelPermissions.perms_map['POST'],
        'PUT': permissions.DjangoModelPermissions.perms_map['PUT'],
        'PATCH': permissions.DjangoModelPermissions.perms_map['PATCH'],
        'DELETE': permissions.DjangoModelPermissions.perms_map['DELETE'],
    }
