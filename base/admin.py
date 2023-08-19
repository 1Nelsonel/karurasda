from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','updated','updated')
admin.site.register(Category, CategoryAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','category','host','description')
    prepopulated_fields = {"slug": ("title",)} #new
    readonly_fields = ('slug',)  # Make the 'slug' field uneditable

admin.site.register(Blog, BlogAdmin)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'eventDate', 'startTime', 'endTime')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category')
    


admin.site.site_header = "Karura SDA Administration"
admin.site.site_title = "Karura SDA Admin Portal"
admin.site.index_title = "Karura SDA Admin Portal"