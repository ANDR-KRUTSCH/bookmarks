from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

# Create your models here.
class Action(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(to=ContentType, on_delete=models.CASCADE, blank=True, null=True, related_name='target_obj')
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey(ct_field='target_ct', fk_field='target_id')

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
            models.Index(
                fields=(
                    'target_ct',
                    'target_id',
                )
            ),
        )