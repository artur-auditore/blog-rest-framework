from django.shortcuts import render, redirect
# Create your views here.
import json
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

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

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-detail'

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-list'

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-detail'

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

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
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
        Profile.objects.create(name=name, email=email, address=address)

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