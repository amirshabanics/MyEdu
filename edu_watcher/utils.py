import imp
from rest_framework import serializers
from .models import User


def get_or_create_user_by_telegram_use_id(telegram_user_id: int) -> User:
    if not telegram_user_id:
        raise serializers.ValidationError({'id': 'is Required.'})

    user = User.objects.get_or_create(telegram_user_id=telegram_user_id)
    return user
