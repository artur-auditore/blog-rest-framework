from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
# Create your views here.
import json
from rest_framework import generics, status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from app.permissions import *
from .serializers import *

class AddressList(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    name = 'address-list'

class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    name = 'address-detail'

class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-list'

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-detail'

class ProfilePostList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePostSerializer
    name = 'profile-posts-list'

class ProfilePostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePostSerializer
    name = 'profile-posts-detail'

class PostCommentList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCommentSerializer
    name = 'post-comment-list'

class PostCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class =  PostCommentSerializer
    name = 'post-comment-detail'

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-list'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-detail'
    permission_classes = (IsUserOrReadOnly,)

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    name = 'comment-list'

    def get_queryset(self):
        post = self.kwargs['pk']
        return Comment.objects.filter(post=post)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    #queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-detail'
    lookup_url_kwarg = 'id'
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        post = self.kwargs['pk']
        return Comment.objects.filter(post=post)

class ProfileCount(APIView):
    name = 'profile-count'

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        posts = profile.posts.all()
        comments = []
        for post in posts:
            comments.extend(post.comments.all())
        return Response({
            'pk': pk,
            'name': profile.name,
            'total_posts': len(posts),
            'total_comments': len(comments)
        })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly,)
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly,)

class CustomAuthToken(ObtainAuthToken):
    name = 'api-token'
    throttle_scope = 'api-token'
    throttle_classes = [ScopedRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        self.check_throttles(request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        return  Response({'token': token.key, 'user_id': user.pk, 'email': user.email})

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse(UserList.name, request=request),
            'profiles': reverse(ProfileList.name, request=request),
            'address': reverse(AddressList.name, request=request),
            'posts': reverse(PostList.name, request=request),
            'profile-posts': reverse(ProfilePostList.name, request=request),
            'comments': reverse(PostCommentList.name, request=request),
            'profile-count:': reverse(ProfileCount.name, request=request),
        })


def import_data():

    data = json.load(open('db.json'))

    for user in data['users']:
        ad = user['address']
        address = Address(street=ad['street'], city=ad['city'], suite=ad['suite'], zipcode=ad['zipcode'])

        address.save()

        name = user['name']
        email = user['email']
        user = User.objects.create(username=name, email=email, password="senha")
        Profile.objects.create(name=name, email=email, address=address, user=user)


    for post in data['posts']:
        profile = Profile.objects.get(id=post['userId'])
        Post.objects.create(title=post['title'], body=post['body'], profile=profile)

    for comment in data['comments']:
        post = Post.objects.get(id=comment['postId'])
        Comment.objects.create(id=comment['id'],
                               name=comment['name'],
                               email=comment['email'],
                               body=comment['body'],
                               post=post)