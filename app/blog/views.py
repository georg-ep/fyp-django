from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.viewsets import ViewSet

from blog.models import Post, PostImage, PostComment
from blog.serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, PostImagesSerializer, \
    PostImagesUpdateSerializer, PostCommentCreateSerializer, PostCommentsSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsOwnerPostRelatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.post.user == request.user


class PostListView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(status=1).order_by("-created_on")


class PostOwnerDetail(RetrieveAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.order_by("-created_on")
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]


class PostDetailView(RetrieveAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class PostUpdateDestroyView(UpdateAPIView, DestroyAPIView, ViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.order_by("-created_on")
    parser_classes = [MultiPartParser, FileUploadParser]
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]


class PostCreateView(CreateAPIView, ViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.order_by("-created_on")
    parser_classes = [MultiPartParser, FileUploadParser]
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class ImageCreateView(CreateAPIView):
    serializer_class = PostImagesSerializer
    queryset = PostImage.objects.all()
    parser_classes = [MultiPartParser, FileUploadParser]
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class ImageDeleteUpdateView(DestroyAPIView, UpdateAPIView, ViewSet):
    serializer_class = PostImagesUpdateSerializer
    queryset = PostImage.objects.all()
    parser_classes = [MultiPartParser, FileUploadParser]
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerPostRelatedOrReadOnly
    ]


class PostCommentCreateView(CreateAPIView):
    serializer_class = PostCommentCreateSerializer
    queryset = PostComment.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class PostCommentListView(ListAPIView):
    serializer_class = PostCommentsSerializer
    queryset = PostComment.objects.order_by('-created_on').all()

    def get_queryset(self):
        filter_kwargs = {'post__slug': self.kwargs.get('slug')}
        return self.queryset.filter(**filter_kwargs)


class PostCommentDeleteView(DestroyAPIView):
    serializer_class = PostCommentsSerializer
    queryset = PostComment.objects.order_by('-created_on').all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerPostRelatedOrReadOnly
    ]
