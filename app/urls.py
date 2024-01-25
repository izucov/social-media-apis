from django.urls import path
from .views import RegisterUserAPIView, Search, FriendList, FriendRequestView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("auth", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("register", RegisterUserAPIView.as_view(), name="register"),
    path("friends", FriendList.as_view(), name="friends"),
    path("friends/requests", FriendRequestView.as_view(), name="friend_request"),
    path(
        "friends/requests/<int:request_id>",
        FriendRequestView.as_view(),
        name="friend_request_action",
    ),
    path("search", Search.as_view(), name="search"),
]
