from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(
        source='user.username'
    )

    class Meta:
        model = Message
        fields = ('id', 'username', 'timestamp', 'message')


class BoardSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = Board
        fields = ('name', 'messages')


class JoinBoardNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source='board'
    )

    class Meta:
        model = Join
        fields = ('name', )


class BoardNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('name', )


class UserSerializer(serializers.ModelSerializer):
    boards = JoinBoardNameSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'boards')
