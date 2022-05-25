from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowUsersSerializer

#, FullUserSerializer sdffdsfdsfd




class FollowUserViewSet(UserViewSet):

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, id=id)

        if user == following:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, following=following).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=user, following=following)
        serializer = FollowUsersSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post', 'delete'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def del_subscribe(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, id=id)
        if user == following:
            return Response({
                'errors': 'Вы не можете отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.filter(user=user, following=following)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowUsersSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)






# class FollowUserViewSet(UserViewSet):
#     serializer_class = FullUserSerializer

#     def user_subscribe(self, serializer, id=None):
#         following_user = get_object_or_404(User, id=id)

#         if self.request.user == following_user:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         follow = Follow.objects.get_or_create(
#             user=self.request.user,
#             following=following_user
#         )

#         return Response(FollowUsersSerializer(follow[0]).data)

#     def user_unsubscribe(self, serializer, id=None):
#         following_user = get_object_or_404(User, id=id)

#         deleted_subscriptions = Follow.objects.filter(
#             user=self.request.user,
#             following=following_user
#         ).delete()

#         if deleted_subscriptions[0] > 0:
#             return Response(status=status.HTTP_204_NO_CONTENT)

#         return Response(status=status.HTTP_404_NOT_FOUND)

#     @action(
#         detail=True,
#         methods=['post', 'delete'],
#         permission_classes=[permissions.IsAuthenticated]
#     )
#     def subscribe(self, serializer, id=None):
#         if self.request.method == 'DELETE':
#             return self.user_unsubscribe(serializer, id)
#         return self.user_subscribe(serializer, id)

#     @action(
#         detail=False,
#         methods=['get'],
#         permission_classes=[permissions.IsAuthenticated]
#     )
#     def subscriptions(self, serializer):
#         follow_list = Follow.objects.filter(user=self.request.user)
#         page = self.paginate_queryset(follow_list)
#         serializer = FollowUsersSerializer(page, many=True)
#         return self.get_paginated_response(serializer.data)
