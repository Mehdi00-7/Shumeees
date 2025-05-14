from __future__ import annotations
from typing import Any, Dict
from .models import User, Hobby
from rest_framework import serializers


class HobbySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hobby
        fields = ["url", "name"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    hobby_list: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "age",
            "hobbies",
            "hobby_list",
            "friends",
            "sent_friend_requests",
            "received_friend_requests",
        ]
        extra_kwargs: Dict[str, Any] = {
            "sent_friend_requests": {"required": False},
            "received_friend_requests": {"required": False},
            "friends": {"required": False},
        }

    def get_hobby_list(self, obj: User) -> list[Dict[str, Any]]:
        """
        Returns a serialized list of the user's hobbies.
        """
        request = self.context.get("request")
        hobbies = Hobby.objects.filter(user=obj)
        return HobbySerializer(hobbies, many=True, context={"request": request}).data
