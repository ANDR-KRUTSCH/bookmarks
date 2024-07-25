from typing import Iterable

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

User = get_user_model()

# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='images_created')
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(to=User, blank=True, related_name='images_liked')

    class Meta:
        ordering = (
            '-created',
        )
        indexes = (
            models.Index(
                fields=(
                    '-created',
                )
            ),
        )
    
    def save(self, force_insert: bool = False, force_update: bool = False, using: str | None = None, update_fields: Iterable[str] | None = None) -> None:
        if not self.slug:
            self.slug = slugify(value=self.title)
        return super().save(force_insert, force_update, using, update_fields)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('images:detail', args=[self.pk, self.slug])