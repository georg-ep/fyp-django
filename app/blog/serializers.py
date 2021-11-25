from rest_framework import serializers

from blog.models import Post, PostImage, PostComment
from user.models import User


class CurrentUserDefault(object):

    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id

    def __repr__(self):
        return self.__class__.__name__


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', "surname", "email", "avatar")


class PostImagesSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = PostImage
        fields = "__all__"


class PostImagesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('title', 'position')


class PostCommentCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=CurrentUserDefault())
    user = serializers.CharField(source='user.email', read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.filter(status=1).all())

    class Meta:
        model = PostComment
        fields = ('user_id', 'user', 'text', 'post')


class PostCommentsSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, model):
        return PostUserSerializer(
            instance=model.user
        ).data

    class Meta:
        model = Post
        fields = ("id", 'image_thumb', "title", "slug", "created_on", "content", "user")


class PostDetailSerializer(serializers.ModelSerializer):
    images = PostImagesSerializer(many=True)
    user = PostUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=CurrentUserDefault())
    user = serializers.CharField(source='user.email', read_only=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'image', 'slug', 'title', 'content', 'status', 'user_id', 'user')


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'image', 'slug', 'title', 'content', 'status')
