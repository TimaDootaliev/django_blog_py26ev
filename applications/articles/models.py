from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Article(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    )


    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='articles', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    tag = models.ManyToManyField("Tag", related_name='articles')
    status = models.CharField(max_length=6, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = "Статьи"
        ordering = ['created_at']
    
    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self) -> str:
        return self.title
