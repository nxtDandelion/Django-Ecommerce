from django.db import models
from django.utils import timezone


class GetOrNoneQuerySet(models.QuerySet):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class GetOrNoneManager(models.Manager):
    def get_queryset(self):
        return GetOrNoneQuerySet(self.model)

    def get_or_none(self, **kwargs):
        return self.get_queryset().get_or_none(**kwargs)


class IsDeleteQuerySet(GetOrNoneQuerySet):
    def delete(self, hard_delete=False):
        if hard_delete:
            return super().delete()
        else:
            return self.update(is_deleted=True, deleted_at=timezone.now())


class IsDeleteManager(GetOrNoneManager):
    def get_queryset(self):
        return IsDeleteQuerySet(self.model).filter(is_deleted=False)

    def unfiltered(self):
        return IsDeleteQuerySet(self.model)

    def hard_delete(self):
        return self.unfiltered().delete(hard_delete=True)
