from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *
from django.utils.html import format_html
from PIL import Image
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.utils.translation import gettext_lazy as _


# Register your models here.
class CategoryAdmin(ModelAdmin):
    list_display = ('name','updated','updated')
admin.site.register(Category, CategoryAdmin)

class BlogAdmin(ModelAdmin):
    list_display = ('title','category','host',)
    prepopulated_fields = {"slug": ("title",)} #new

admin.site.register(Blog, BlogAdmin)

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('blog', 'user', 'email',)
    list_filter = ('blog', 'user',)
    search_fields = ('blog',)

@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('title', 'venue', 'eventDate', 'startTime', 'endTime')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Leader)
class LeaderAdmin(ModelAdmin):
    list_display = ('name', 'position', 'category')

@admin.register(Ministry)
class MinistryAdmin(ModelAdmin):
    list_display = ('name', 'updated', 'created')
    search_fields = ('name', 'content')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Gallery)
class GalleryAdmin(ModelAdmin):
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
class SermonAdmin(ModelAdmin):
    list_display = ('videolink', 'updated', 'created')
    list_filter = ('updated', 'created')
    search_fields = ('videolink',)
    date_hierarchy = 'created'

@admin.register(Song)
class SongAdmin(ModelAdmin):
    list_display = ('videolink', 'updated', 'created')
    list_filter = ('updated', 'created')
    search_fields = ('videolink',)
    date_hierarchy = 'created'

@admin.register(LiveStream)
class LiveStramAdmin(ModelAdmin):
    list_display = ('videolink', 'updated', 'created')
    list_filter = ('updated', 'created')
    search_fields = ('videolink',)
    date_hierarchy = 'created'

@admin.register(Carousel)
class CarouselAdmin(ModelAdmin):
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
class FamilyAdmin(ModelAdmin):
    list_display = ('name','slug', 'updated', 'created')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Member)
class MemberAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'family', 'memberNumber', 'updated', 'created')
    search_fields = ('name', 'family', 'admision')
    prepopulated_fields = {'slug': ('name',)}


# Unregister default User and Group admins to replace with Unfold versions
admin.site.unregister(User)
admin.site.unregister(Group)

# User Admin with Unfold styling
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Custom User Admin with Unfold styling"""
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_active', 'groups'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.resolver_match.url_name == 'auth_user_changelist':
            qs = qs.only('id', 'username', 'email', 'first_name', 'last_name',
                        'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
        return qs


# Group Admin with Unfold styling
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Custom Group Admin with Unfold styling"""
    list_display = ('name', 'member_count')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def member_count(self, obj):
        """Display number of users in the group"""
        count = obj.user_set.count()
        return format_html(
            '<span style="background: #3b82f6; color: white; padding: 4px 8px; '
            'border-radius: 4px; font-size: 11px; font-weight: 600;">{} members</span>',
            count
        )
    member_count.short_description = _('Members')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.resolver_match.url_name == 'auth_group_change':
            qs = qs.prefetch_related('permissions', 'user_set')
        return qs


admin.site.site_header = "Karura SDA Administration"
admin.site.site_title = "Karura SDA Admin Portal"
admin.site.index_title = "Karura SDA Admin Portal"