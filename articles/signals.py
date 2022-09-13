from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from articles.models import Article


@receiver(pre_save, sender=Article)
def add_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.title)
        instance.slug = slug
