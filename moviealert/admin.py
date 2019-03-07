from django.contrib import admin
from .models import Region, Task
# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'alias']
    search_fields = ['name', 'alias']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie_name', 'city', 'movie_language', 'movie_dimension',
                    'movie_date', 'task_completed', 'search_count', 'dropped']
    search_fields = ['user', 'movie_name']
    list_filter = ['movie_language', 'movie_dimension', 'task_completed', 'dropped']
    autocomplete_fields = ['city']
