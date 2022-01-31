from django.db import models

from pyspark import F

# Create your models here.


class Department(models.Model):
    name = models.CharField(null=False, max_length=256)
    number = models.PositiveIntegerField(null=False, blank=False, unique=True)


class Course(models.Model):
    course_id = models.PositiveIntegerField(null=False, blank=False)
    group = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        unique_together = ('course_id', 'group',)

# Extend from abstact user django
class User(models.Model):
    telegram_user_id = models.PositiveIntegerField(null=False, blank=False)
    edu_token = models.CharField(max_length=512, null=True)
    wathDepartment = models.ManyToManyField(
        Department, through='WatchDepartment',
        through_fields=('user', 'department')
    )
    wathCourse = models.ManyToManyField(
        Department, through='WatchCourse',
        through_fields=('user', 'course')
    )


class WatchAction(models.Model):
    name = models.CharField(null=False, unique=True)


class Watch(models.Model):
    user = models.ForeignKey(User)
    actions = models.ManyToManyField(WatchAction)


class WatchDepartment(Watch):
    department = models.ForeignKey(Department, related_name='watchList')


class WatchCourse(Watch):
    course = models.ForeignKey(Course, related_name='watchList')
