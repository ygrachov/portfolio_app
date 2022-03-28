from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class ForumList(models.Model):
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, 'the field must contain at list 3 characters!')]
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_owner')
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256,
                                    help_text='The MIMEType of the file', null=True, blank=True)
    comment = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comments')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Fav', related_name='favorite_forum')

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment = models.TextField(
        validators=[MinLengthValidator(3, 'the field must contain at list 3 characters!')]
    )
    forum = models.ForeignKey(ForumList, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Fav(models.Model):
    forum = models.ForeignKey(ForumList, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('forum', 'user')
