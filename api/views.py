from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import *

err_invalid_input = Response(
    {'message': 'Cannot create user, please recheck input fields'},
    status=status.HTTP_400_BAD_REQUEST,
)
err_no_permission = Response(
    {'message': 'You do not have permission to perform this action'},
    status=status.HTTP_403_FORBIDDEN,
)
err_not_found = Response(
    {'message': 'Not found'},
    status=status.HTTP_404_NOT_FOUND,
)
err_not_allowed = Response(
    {'message': 'Operation Not Allowed'},
    status=status.HTTP_405_METHOD_NOT_ALLOWED
)


def check_arguments(request, args):
    # check for missing arguments
    missing = []
    for arg in args:
        if arg not in request.data:
            missing.append(arg)
    if missing:
        print(missing)
        response = {
            'Missing argument': '%s' % ', '.join(missing),
        }
        return 1, Response(response, status=status.HTTP_400_BAD_REQUEST)
    return 0,




# class UserViewSet(viewsets.ModelViewSet):
#     queryset = ExtendedUser.objects.all()
#     serializer_class = ExtendedUserSerializer
#
#     def create(self, request):

#
#     def list(self, request):

#
#     def retrieve(self, request, pk=None):

#
#     @action(methods=['POST'], detail=True)
#     def change_password(self, request, pk=None):

