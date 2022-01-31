from ast import Try
from dataclasses import fields
from multiprocessing.connection import wait
import django
from django.shortcuts import get_object_or_404


from rest_framework import serializers

from edu_watcher.utils import get_or_create_user_by_telegram_use_id

from .models import Course, Department, User, WatchAction, WatchCourse, WatchDepartment


class WatchActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchAction
        fields = ['name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'number']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'group']


class WatchDepartmentSerializer(serializers.ModelSerializer):
    actions = WatchActionSerializer(many=True, read_only=True)
    depatment = DepartmentSerializer(read_only=True)

    department_number = serializers.IntegerField(
        write_only=True, required=True)
    action = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = WatchDepartment
        fields = ['actions', 'department']

    def create(self, validated_data):
        if 'user_id' not in self.request.kwargs:
            raise serializers.ValidationError({'user_id': 'is Required.'})

        user = get_or_create_user_by_telegram_use_id(
            self.request.kwargs['user_id'])
        department_number = validated_data.get('depatment_number')
        action = validated_data.get('action')
        try:
            department = Department.objects.get(number=department_number)
        except:
            raise serializers.ValidationError({'user_id': 'is not Valid.'})

        watchDepartment = WatchDepartment.objects.get_or_create(
            user=user, departmen=department)

        action = get_object_or_404(WatchAction, name=action)
        watchDepartment.actions.add(action)
        watchDepartment.save()
        return watchDepartment


class WatchCourseSerializer(serializers.ModelSerializer):
    actions = WatchActionSerializer(many=True)
    course = CourseSerializer()

    course_id = serializers.IntegerField(
        write_only=True, required=True)
    group = serializers.IntegerField(
        write_only=True, required=True)
    action = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = WatchCourse
        fields = ['actions', 'course']

    def create(self, validated_data):
        if 'user_id' not in self.request.kwargs:
            raise serializers.ValidationError({'user_id': 'is Required.'})

        user = get_or_create_user_by_telegram_use_id(
            self.request.kwargs['user_id'])
        course_id = validated_data.get('course_id')
        group = validated_data.get('group')
        action = validated_data.get('action')
        try:
            course = Course.objects.get(course_id=course_id, group=group)
        except:
            raise serializers.ValidationError({'user_id': 'is not Valid.'})

        watchCourse = WatchCourse.objects.get_or_create(
            user=user, course=course)

        action = get_object_or_404(WatchAction, name=action)
        watchCourse.actions.add(action)
        watchCourse.save()
        return watchCourse


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['telegram_user_id', 'edu_token']
