from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# blog category
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    

# blogs
class Blog(models.Model):
    host = models.CharField(max_length=200, null=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, db_index=True)
    title = models.CharField(max_length=200, db_index=True)
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
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(null=False, unique=True, db_index=True)
    venue = models.CharField(max_length=100, db_index=True)
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
        ('Pastors', 'Pastors'),
        ('Elder', 'Elder'),
        ('Other Church Leaders', 'Other Leader'),
    )

    name = models.CharField(max_length=100, db_index=True)
    position = models.CharField(max_length=100, db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='static/leader')  # Requires `Pillow` library

    def __str__(self):
        return self.name

# ministries
class Ministry(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(null=False, unique=True, db_index=True)
    image = models.ImageField(upload_to="ministry")
    content =  models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ministry', kwargs={'slug': self.slug})
    
# ===================================================================
# contact model
# ===================================================================
class Contact(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20, null=True)
    body = models.TextField()   
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

# ===================================================================
# Gallary
# ===================================================================
class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery')
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']
    
