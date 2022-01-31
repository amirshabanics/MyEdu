from curses.ascii import US
from os import stat
from django.shortcuts import get_object_or_404, render

from edu_watcher.utils import get_or_create_user_by_telegram_use_id

from rest_framework import status
from .serializers import UserInfoSerializer, WatchDepartmentSerializer
from .models import Department, User, WatchDepartment
from edu_watcher import serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
#  Edit after implement auth


class CreateOrGetUserInfo(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer

    def get_object(self):
        if 'id' not in self.kwargs:
            raise serializers.ValidationError({'id': 'is Required.'})

        return get_or_create_user_by_telegram_use_id(self.kwargs['id'])


class UpdateToken(APIView):

    def post(self, request, format=None):
        if 'id' not in self.kwargs:
            raise serializers.ValidationError({'id': 'is Required.'})

        user = get_or_create_user_by_telegram_use_id(self.kwargs['id'])

        if 'token' not in self.kwargs:
            raise serializers.ValidationError({'token': 'is Required.'})
        user.edu_token = self.kwargs['token']
        user.save()

        return Response(status=status.HTTP_200_OK)


class DepartmentActions(generics.ListCreateAPIView):
    serializer_class = WatchDepartmentSerializer

    def get_queryset(self):
        if 'id' not in self.kwargs:
            raise serializers.ValidationError({'id': 'is Required.'})

        user = get_or_create_user_by_telegram_use_id(self.kwargs['id'])

        return WatchDepartment.objects.filter(user=user)


class DeleteWatchDepartment(APIView):
    def get(self, request, format=None):

        if 'user_id' not in self.kwargs:
            raise serializers.ValidationError({'user_id': 'is Required.'})
        user = get_or_create_user_by_telegram_use_id(self.kwargs['user_id'])

        if 'department_number' not in self.kwargs:
            raise serializers.ValidationError(
                {'department_number': 'is Required.'})
        department = get_object_or_404(
            Department, numebr=self.kwargs['department_number'])
        watchDepartment = get_object_or_404(
            WatchDepartment, department=department, user=user)
        watchDepartment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
