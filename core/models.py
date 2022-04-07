from email.policy import default
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



# Create your models here.
class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    coverpic = models.ImageField(upload_to='post', blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    date = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICE, max_length=10, default='draft')

    def save(self):
        self.date = f"{self.publish.strftime('%B')} {self.publish.strftime('%D').split('/')[1]} 20{self.publish.strftime('%D').split('/')[2]}"
        super(Post, self).save()

    class Meta:
        ordering = ('-publish'),

    def __str__(self) -> str:
        return self.title



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.message}"