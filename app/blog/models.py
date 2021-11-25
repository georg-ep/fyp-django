from io import BytesIO

from django.db import models

# Create your models here.
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from core.models import safe_file_path
from user.models import User

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + '_' + get_random_string(length=4)
    return unique_slug


def create_thumbnail(model):
    # original code for this method came from
    # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

    # If there is no image associated with this.
    # do not create thumbnail
    if not model.image:
        return

    from PIL import Image
    from django.core.files.uploadedfile import SimpleUploadedFile
    import os

    # Set our max thumbnail size in a tuple (max width, max height)
    thumbnail_size = (200, 200)

    django_type = model.image.file.content_type

    if django_type == 'image/jpeg':
        pil_type = 'jpeg'
        file_extension = 'jpg'
    elif django_type == 'image/png':
        pil_type = 'png'
        file_extension = 'png'

    # Open original photo which we want to thumbnail using PIL's Image
    image = Image.open(model.image)

    # We use our PIL Image object to create the thumbnail, which already
    # has a thumbnail() convenience method that contrains proportions.
    # Additionally, we use Image.ANTIALIAS to make the image look better.
    # Without antialiasing the image pattern artifacts may result.
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)

    # Save the thumbnail
    temp_handle = BytesIO()
    image.save(temp_handle, pil_type)
    temp_handle.seek(0)

    # Save image to a SimpleUploadedFile which can be saved into
    # ImageField
    suf = SimpleUploadedFile(os.path.split(model.image.name)[-1],
                             temp_handle.read(), content_type=django_type)
    # Save SimpleUploadedFile into image field
    model.image_thumb.save(
        '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], file_extension),
        suf,
        save=False
    )


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to=safe_file_path, blank=True, null=True)
    image_thumb = models.ImageField(upload_to=safe_file_path, blank=True, null=True, editable=False)

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        create_thumbnail(self)
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=safe_file_path, blank=True, null=True)
    image_thumb = models.ImageField(upload_to=safe_file_path, blank=True, null=True, editable=False)
    position = models.PositiveIntegerField(default=99999999)
    title = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('-position',)

    def save(self, *args, **kwargs):
        create_thumbnail(self)

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True

        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(PostImage, self).save(force_update=force_update)


class PostComment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_on = models.DateTimeField(auto_now_add=True)
