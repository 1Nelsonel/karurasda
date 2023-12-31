from django.contrib import admin
from .models import *
from django.utils.html import format_html
from PIL import Image


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','updated','updated')
admin.site.register(Category, CategoryAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','category','host',)
    prepopulated_fields = {"slug": ("title",)} #new

admin.site.register(Blog, BlogAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'email',)
    list_filter = ('blog', 'user',)
    search_fields = ('blog',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'eventDate', 'startTime', 'endTime')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category')

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated', 'created')
    search_fields = ('name', 'content')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('display_image', )
    list_filter = ('updated', 'created')
    date_hierarchy = 'created'

    def save_model(self, request, obj, form, change):
        # Get the uploaded image file
        uploaded_image = form.cleaned_data['image']

        # Get the original filename and extension
        original_filename = uploaded_image.name
        file_extension = original_filename.split('.')[-1]

        # Open the image using PIL
        image = Image.open(uploaded_image)

        # Calculate the desired width and height for a 16:9 aspect ratio
        desired_width = 16
        desired_height = 9
        max_dimension = 1000  # Set your desired maximum dimension here

        # Calculate the new dimensions while maintaining the aspect ratio
        width, height = image.size
        if width / desired_width > height / desired_height:
            new_width = max_dimension
            new_height = int((max_dimension * height) / width)
        else:
            new_height = max_dimension
            new_width = int((max_dimension * width) / height)

        # Resize the image to the calculated dimensions
        image.thumbnail((new_width, new_height), Image.LANCZOS)

        # Save the resized image with the new filename
        obj.image.name = f'karura-sda{Gallery.objects.count() + 1}.{file_extension}'
        image.save(obj.image.path)

        super().save_model(request, obj, form, change)

    def display_image(self, obj):
        return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
    display_image.short_description = 'Image Preview'

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('videolink', 'updated', 'created')
    list_filter = ('updated', 'created')
    search_fields = ('videolink',)
    date_hierarchy = 'created'

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('videolink', 'updated', 'created')
    list_filter = ('updated', 'created')
    search_fields = ('videolink',)
    date_hierarchy = 'created'

@admin.register(LiveStream)
class LiveStramAdmin(admin.ModelAdmin):
    list_display = ('videolink', 'updated', 'created')
    list_filter = ('updated', 'created')
    search_fields = ('videolink',)
    date_hierarchy = 'created'

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'created')
    list_filter = ('updated', 'created')
    search_fields = ('title', 'subtitle')
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        # Get the uploaded image file
        uploaded_image = form.cleaned_data['image']

        # Get the original filename and extension
        original_filename = uploaded_image.name
        file_extension = original_filename.split('.')[-1]

        # Create a new filename with an incremental number
        obj.image.name = f'karura-sda{Gallery.objects.count() + 1}.{file_extension}'

        # Resize the uploaded image (adjust dimensions as needed)
        max_dimension = 1000  # Set your desired maximum dimension here
        image = Image.open(uploaded_image)
        image.thumbnail((max_dimension, max_dimension), Image.LANCZOS)
        image.save(obj.image.path)

        super().save_model(request, obj, form, change)

    def display_image(self, obj):
        return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
    display_image.short_description = 'Image Preview'

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name','slug', 'updated', 'created')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'family', 'memberNumber', 'updated', 'created')
    search_fields = ('name', 'family', 'admision')


admin.site.site_header = "Karura SDA Administration"
admin.site.site_title = "Karura SDA Admin Portal"
admin.site.index_title = "Karura SDA Admin Portal"