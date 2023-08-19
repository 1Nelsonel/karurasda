from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# blog category
class Category(models.Model):
    name = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
# blogs
class Blog(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='static/blog', null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title[0:50]

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'slug': self.slug})
    
# event
class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    venue = models.CharField(max_length=100)
    eventDate = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='static/event', null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title[0:50]

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'slug': self.slug})
    
# leader
class Leader(models.Model):
    CATEGORY_CHOICES = (
        ('pastor', 'Pastor'),
        ('elder', 'Elder'),
        ('other', 'Other Leader'),
    )

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='static/leader')  # Requires `Pillow` library

    def __str__(self):
        return self.name