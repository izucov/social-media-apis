from django.contrib.auth.models import User
from django.db import models

from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Profile, FriendRequest, FriendRequestStatus
from .serializers import RegisterSerializer, UserSerializer, FriendRequestSerializer
from .throttling import CustomThrottle


class FriendList(generics.ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)

        return profile.friend_list


class FriendRequestView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (CustomThrottle,)

    def get(self, request):
        friend_requests = FriendRequest.objects.filter(
            user=request.user, status=FriendRequestStatus.PENDING
        )

        serializer = FriendRequestSerializer(friend_requests, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = User.objects.get(id=int(request.data.get("user")))

        try:
            FriendRequest.objects.get(
                user=user,
                sender=request.user,
                status__in=[
                    FriendRequestStatus.ACCEPTED,
                    FriendRequestStatus.PENDING,
                ],
            )

            response = Response(status=400)

        except FriendRequest.DoesNotExist:
            FriendRequest.objects.create(
                user=user, sender=request.user, status=FriendRequestStatus.PENDING
            )

            response = Response(status=201)

        return response

    def put(self, request, request_id):
        friend_request = FriendRequest.objects.get(id=request_id)
        action = request.data.get("action")

        if friend_request.user != request.user:
            return Response(status=403)

        if friend_request.status != FriendRequestStatus.PENDING:
            return Response(status=400)

        if action == "accept":
            friend_request.status = FriendRequestStatus.ACCEPTED
            friend_request.save()

        elif action == "reject":
            friend_request.status = FriendRequestStatus.REJECTED
            friend_request.save()

        return Response(status=200)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class Search(generics.ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()

        search_query = self.request.query_params.get("query", "")

        if exact_search_qs := queryset.filter(email__iexact=search_query):
            queryset = exact_search_qs
        else:
            queryset = queryset.filter(
                models.Q(email__icontains=search_query)
                | models.Q(first_name__icontains=search_query)
                | models.Q(last_name__icontains=search_query)
            )

        return queryset
