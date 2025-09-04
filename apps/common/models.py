import uuid
from django.db import models
from django.utils import timezone

from apps.common.managers import GetOrNoneManager, IsDeleteManager


class BaseModel(models.Model):
    """
    Base class that includes common fields and methods

    Attributes:
        id (UUIDField): Unique identifier for the model instance
        created_at (DateTimeField): Timestamp when the instance was created
        updated_at (DateTimeField): Timestamp when the instance was last updated
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True


class IsDeletedModel(BaseModel):
    """
    Model that includes delete() and hard_delete() methods

    Attributes:
        is_deleted (BooleanField): Mark if the instance was soft-deleted (not deleted in database);
        deleted_at (DateTimeField): Timestamp when the instance was soft-deleted (not deleted in database)
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    objects = IsDeleteManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
