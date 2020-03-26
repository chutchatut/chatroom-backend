from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('users', UserViewSet)
router.register('boards', BoardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
