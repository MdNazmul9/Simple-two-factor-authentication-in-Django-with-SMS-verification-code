from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializer import ChangePasswordSerializer, ResetPasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ChangePasswordSerializer


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        alldatas = {}
        if serializer.is_valid(raise_exception=True):
            mname = serializer.save()
            alldatas['data'] = 'Successfully registered'
            # print(alldatas)
            return Response(alldatas)
        return Response('failed retry after some time')
