from __future__ import annotations
from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class Hobby(models.Model):
    name: str = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    date_of_birth: Optional[date] = models.DateField("Date of Birth", null=True)
    hobbies: models.ManyToManyField[Hobby] = models.ManyToManyField(
        Hobby, blank=True, verbose_name="Hobbies"
    )
    friends: models.ManyToManyField[User] = models.ManyToManyField("self", blank=True)
    sent_friend_requests: models.ManyToManyField[User] = models.ManyToManyField(
        "self", symmetrical=False, related_name="received_friend_requests", blank=True
    )

    def send_friend_request(self, user: User) -> bool:
        if user == self:
            raise ValueError("You cannot send a friend request to yourself.")
        if user in self.friends.all():
            raise ValueError("This user is already your friend.")
        if user in self.sent_friend_requests.all():
            raise ValueError("Friend request already sent.")
        print(f"Adding {user.username} to {self.username}'s friend requests.")
        self.sent_friend_requests.add(user)
        print(
            f"{self.username}'s sent friend requests: {[u.username for u in self.sent_friend_requests.all()]}"
        )
        self.save()  # Ensure changes are saved
        return True

    def accept_friend_request(self, user: User) -> bool:
        if user in self.received_friend_requests.all():
            self.received_friend_requests.remove(user)
            self.friends.add(user)
            user.friends.add(self)
            return True
        return False

    def decline_friend_request(self, user: User) -> bool:
        if user in self.received_friend_requests.all():
            self.received_friend_requests.remove(user)
            return True
        return False

    def __str__(self) -> str:
        hobbies_str = ", ".join(hobby.name for hobby in self.hobbies.all())
        return f"{self.username} - Hobbies: {hobbies_str}"

    @property
    def age(self) -> Optional[int]:
        if self.date_of_birth is None:
            return None
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
