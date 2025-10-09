from django.contrib import admin
from .models import Blog, MsPost, MsVideo
# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'created_at', 'updated_at']
    
@admin.register(MsPost)   
class MsPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at']
    
    
@admin.register(MsVideo)   
class MsVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'video_url', 'created_at', 'updated_at']