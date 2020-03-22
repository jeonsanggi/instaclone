from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    # class Meta를 통해 model 전체의 옵션을 잡아줌
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
