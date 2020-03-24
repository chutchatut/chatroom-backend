from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

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


class UserViewSet(viewsets.ModelViewSet):

    def create(self, request):
        if not request.user.is_staff:
            return err_no_permission
        response = check_arguments(request.data, [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        ])
        if response[0] != 0:
            return response[1]

        username = request.data['username']
        password = request.data['password']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        try:
            User.objects.get(username=username)
            return Response(
                {'message': 'A user with identical username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name,
                                            email=email)
        try:
            user.full_clean()
        except ValidationError:
            user.delete()
            return err_invalid_input
        Token.objects.create(user=user)
        return Response(
            {
                'message': 'A user has been created',
                'result': UserSerializer(user, many=False).data,
            },
            status=status.HTTP_200_OK
        )

    def list(self, request):
        user = request.user
        serializer_class = UserSerializer
        return Response(serializer_class(user, many=False).data,
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        if not request.user.is_staff:
            return err_no_permission
        try:
            user = User.objects.get(username=pk)
        except:
            return err_not_found
        if request.user != user:
            return err_no_permission
        return Response(
            UserSerializer(user, many=False).data,
            status=status.HTTP_200_OK
        )

    @action(methods=['POST'], detail=True)
    def change_password(self, request, pk=None):
        if pk != request.user.username and not request.user.is_staff:
            return err_no_permission
        response = check_arguments(request.data, ['password', ])
        if response[0] != 0:
            return response[1]

        queryset = User.objects.all()
        serializer_class = UserSerializer
        username = pk
        password = request.data['password']

        try:
            user = queryset.get(username=username)
            user.set_password(password)
            user.save()
            return Response(
                {
                    'message': 'Password has been set',
                    'result': serializer_class(user.extended, many=False).data
                },
                status=status.HTTP_200_OK,
            )
        except:
            return err_not_found


class BoardViewSet(viewsets.ModelViewSet):

    def create(self, request):
        response = check_arguments(request.data, ['name'])
        if response[0] != 0:
            return response[1]

        name = request.data['name']

        try:
            Board.objects.get(name=name)
            return Response(
                {'message': 'Board with identical name already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            Board.objects.create(name=name)
            return Response(
                {'message': 'Board created'},
                status=status.HTTP_200_OK
            )

    def list(self, request):
        queryset = Board.objects.all()
        serializer_class = BoardNameSerializer
        return Response(serializer_class(queryset, many=True).data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            board = Board.objects.get(name=pk)
        except:
            return err_not_found
        try:
            join_status = Join.objects.get(
                user=request.user,
                board=board
            )
        except:
            join_status = Join.objects.create(
                user=request.user,
                board=board,
                last_read=0
            )
        last_read = join_status.last_read
        join_status.last_read = board.messages[-1].id
        join_status.save()
        serializer_class = BoardSerializer
        return Response({'last_read': last_read,
                         'boards': serializer_class(board).data},
                        status=status.HTTP_200_OK
                        )

    @action(methods=['POST'], detail=True)
    def post(self, request, pk=None):
        response = check_arguments(request.data, ['message'])
        if response[0] != 0:
            return response[1]
        try:
            board = Board.objects.get(name=pk)
        except:
            return err_not_found
        message = request.data['message']
        Message.objects.create(user=request.user, board=Board, message=message)