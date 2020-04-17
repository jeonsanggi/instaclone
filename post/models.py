from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import re


# Create your models here.
def photo_path(instance, filename):
    from time import strftime
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '{}/{}/{}.{}'.format(strftime('post/%Y/%m/%d/'), instance.author.username, pid, extension)

class Post(models.Model):
    #user 모델의 내용을 외래키로 받아옴
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = ProcessedImageField(upload_to=photo_path,
                                processors=[ResizeToFill(600, 600)],
                                format = 'JPEG',
                                options={'quality': 90})
    content = models.CharField(max_length=140, help_text="최대길이 140자 입력이 가능합니다.")

    tag_set = models.ManyToManyField('Tag', blank=True)

    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True,
                                            related_name = 'like_user_set',
                                            through='Like') # post.like_user_set 으로 접근이 가능해짐
    bookmark_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True,
                                            related_name = 'bookmark_user_set',
                                            through='Bookmark') # post.bookmark_user_set 으로 접근이 가능해짐
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    # class Meta를 통해 model 전체의 옵션을 잡아줌
    class Meta:
        ordering = ['-created_at']

    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.content)

        if not tags:
            return

        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(name=t)
            self.tag_set.add(tag)

    @property
    def like_count(self):
        return self.like_user_set.count()

    @property
    def bookmark_count(self):
        return self.bookmark_user_set.count()

    def __str__(self):
        return self.content


# 좋아요
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'post')
        )

# 북마크
class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'post')
        )

# 댓글
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.content

# 태그
class Tag(models.Model):
    name = models.CharField(max_length=148, unique=True)

    def __str__(self):
        return self.name
