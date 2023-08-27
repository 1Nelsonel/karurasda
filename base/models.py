from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from embed_video.fields import EmbedVideoField


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

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'slug': self.slug})
    
# blog comment
class Comment(models.Model):    
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
    
# event
class Event(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(null=False, unique=True, db_index=True)
    venue = models.CharField(max_length=100, db_index=True)
    topic = models.CharField(max_length=255, null=True, db_index=True)
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
    activity = models.ForeignKey(Event, null=True, db_index=True, on_delete=models.CASCADE,blank=True)
    department = models.ForeignKey(Ministry, on_delete=models.CASCADE, null=True,blank=True)
    date = models.DateField(null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']
    
# ===================================================================
# video model
# ===================================================================
class Sermon(models.Model):
    videolink = EmbedVideoField()
    activity = models.ForeignKey(Event, null=True, db_index=True, on_delete=models.CASCADE,blank=True)
    department = models.ForeignKey(Ministry, on_delete=models.CASCADE, null=True,blank=True)
    date = models.DateField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

class Song(models.Model):
    videolink = EmbedVideoField()
    activity = models.ForeignKey(Event, null=True, db_index=True, on_delete=models.CASCADE,blank=True)
    department = models.ForeignKey(Ministry, on_delete=models.CASCADE, null=True,blank=True)
    date = models.DateField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

class LiveStream(models.Model):
    videolink = EmbedVideoField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

# Carousel
class Carousel(models.Model):
    title = models.CharField(max_length=200, db_index=True)    
    subtitle = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='static/carousel', null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title[0:50]

# ===================================================================
# family
# ===================================================================
class Family(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)  # Use SlugField instead of AutoSlugField
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name[0:50]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

# ===================================================================
# members model
# ===================================================================
class Member(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)  # Use SlugField instead of AutoSlugField
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True)
    memberNumber = models.CharField(max_length=100, db_index=True)
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