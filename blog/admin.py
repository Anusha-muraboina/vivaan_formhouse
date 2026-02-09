from django.contrib import admin

# Register your models here.
# admin.py

from .models import *
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "status",  "published_date", "views_count")
    # list_filter = ("status")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    
# admin.site.register(BlogCategory)
# admin.site.register(BlogTag)
