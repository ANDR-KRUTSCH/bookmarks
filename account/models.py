from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self) -> str:
        return f'Profile of {self.user.username}'


class Contact(models.Model):
    user_from = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='rel_from_set')
    user_to = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True)

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

    def __str__(self) -> str:
        return f'{self.user_from} follows {self.user_to}'


User.add_to_class(name='following', value=models.ManyToManyField(to='self', through=Contact, symmetrical=False, related_name='followers'))