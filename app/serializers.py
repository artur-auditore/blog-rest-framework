from rest_framework import serializers
from .models import *

class AddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Address
        fields = ('street', 'suite', 'city', 'zipcode')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    address = serializers.SlugRelatedField(queryset=Address.objects.all(), slug_field='street')

    class Meta:
        model = Profile
        fields = ('name', 'email', 'address')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='title')

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'post')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.SlugRelatedField(queryset=Profile.objects.all(), slug_field='name')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'body', 'profile', 'comments')

class ProfilePostSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('name', 'address', 'email', 'posts')

class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'body', 'profile', 'comments')