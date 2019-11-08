from django.urls import path
from .views import *
urlpatterns = [
    path('', ApiRoot.as_view(), name=ApiRoot.name),
    path('profile/', ProfileList.as_view(), name=ProfileList.name),
    path('profile/<int:pk>', ProfileDetail.as_view(), name=ProfileDetail.name),
    path('address/', AddressList.as_view(), name=AddressList.name),
    path('address/<int:pk>', AddressDetail.as_view(), name=AddressDetail.name),
    path('profile-post/', ProfilePostList.as_view(), name=ProfilePostList.name),
    path('profile-post/<int:pk>', ProfilePostDetail.as_view(), name=ProfilePostDetail.name),
    path('post-comments/', PostCommentList.as_view(), name=PostCommentList.name),
    path('post-comments/<int:pk>', PostCommentDetail.as_view(), name=PostCommentDetail.name),
    path('posts/', PostList.as_view(), name=PostList.name),
    path('posts/<int:pk>', PostDetail.as_view(), name=PostDetail.name),
    path('posts/<int:pk>/comments', CommentList.as_view(), name=CommentList.name),
    path('posts/<int:pk>/comments/<int:id>', CommentDetail.as_view(), name=CommentDetail.name),
    path('profile-count/', ProfilePostList.as_view(), name=ProfileCount.name),
    path('profile-count/<int:pk>/', ProfileCount.as_view(), name=ProfileCount.name),
]