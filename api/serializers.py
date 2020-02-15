from rest_framework import serializers
from .models import *


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ('review', 'score')


# class ExtendedUserSerializer(serializers.HyperlinkedModelSerializer):
#     username = serializers.CharField(
#         source='base_user.username'
#     )

