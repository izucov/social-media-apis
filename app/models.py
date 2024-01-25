from django.contrib.auth.models import User
from django.db import models


class FriendRequestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def friend_list(self):
        """
        Returns a list of friends of the user.
        """
        # Get distinct list of Users both from user, sender fields of FriendRequest model where status is accepted
        user_recvd_friend_reqs = (
            FriendRequest.objects.filter(
                status=FriendRequestStatus.ACCEPTED,
                user=self.user,
            )
            .values("sender")
            .distinct()
            .values_list("sender", flat=True)
        )

        user_sent_friend_reqs = (
            FriendRequest.objects.filter(
                status=FriendRequestStatus.ACCEPTED,
                sender=self.user,
            )
            .values("user")
            .distinct()
            .values_list("user", flat=True)
        )

        friends = User.objects.filter(
            id__in=user_recvd_friend_reqs.union(user_sent_friend_reqs)
        )

        return friends


class FriendRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="User who received the request+"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="User who sent the request+"
    )
    status = models.CharField(
        max_length=8,
        choices=FriendRequestStatus.choices,
        default=FriendRequestStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} sent a friend request to {self.user}"
