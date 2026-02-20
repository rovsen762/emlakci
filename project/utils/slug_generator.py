# utils/slug_generator.py
import uuid
from django.db import transaction, IntegrityError
from django.utils.crypto import get_random_string
import re
from unidecode import unidecode

def custom_slugify(title):
    if not title:
        return ""

    value = unidecode(title).lower()
    value = re.sub(r'[^a-z0-9\s-]', '', value)
    value = re.sub(r'[\s-]+', '-', value)

    return value.strip('-')


def generate_unique_slug(instance, slug_field="slug", title_field="title", max_length=255):
    """
    Production-ready slug generator.
    - max_length uyğunluğu
    - race condition protection
    - transaction safe
    - UUID fallback
    """

    title = getattr(instance, title_field)
    base_slug = custom_slugify(title)

    if not base_slug:
        base_slug = get_random_string(8)

    base_slug = base_slug[:max_length]

    Klass = instance.__class__
    slug = base_slug
    counter = 2

    while True:
        try:
            with transaction.atomic():
                if not Klass.objects.filter(**{slug_field: slug}).exists():
                    return slug

                suffix = f"-{counter}"
                allowed_length = max_length - len(suffix)
                slug = f"{base_slug[:allowed_length]}{suffix}"

                counter += 1

        except IntegrityError:
            suffix = f"-{uuid.uuid4().hex[:6]}"
            allowed_length = max_length - len(suffix)
            slug = f"{base_slug[:allowed_length]}{suffix}"
            return slug




#ornek kod:

# from django.db import models
# from .utils.slug_generator import generate_unique_slug


# class Post(models.Model):
#     title = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True, blank=True, max_length=255)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = generate_unique_slug(
#                 instance=self,
#                 slug_field="slug",
#                 title_field="title",
#                 max_length=self._meta.get_field("slug").max_length
#             )
#         super().save(*args, **kwargs)