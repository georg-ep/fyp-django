from django.contrib import admin

# Register your models here.
from blog.models import Post, PostComment, PostImage


class PostImageInline(admin.StackedInline):
    model = PostImage


class PostCommentInline(admin.StackedInline):
    model = PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (PostCommentInline, PostImageInline)
