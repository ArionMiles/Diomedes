from django.contrib import admin
from .models import Region, Task, SubRegion, Cinemas
# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'alias']
    search_fields = ['name', 'alias']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['username', 'movie_name', 'city', 'movie_language', 'movie_dimension',
                    'movie_date', 'task_completed', 'search_count', 'dropped']
    search_fields = ['username', 'movie_name']
    list_filter = ['movie_language', 'movie_dimension', 'task_completed', 'dropped']
    autocomplete_fields = ['city']

@admin.register(SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
    list_display = ['region_code', 'sub_region_code', 'sub_region_name']
    search_fields = ['sub_region_name']

@admin.register(Cinemas)
class CinemasAdmin(admin.ModelAdmin):
    list_display = ['venue_code', 'venue_name', 'venue_sub_region_code', 'venue_sub_region_name']
    search_fields = ['venue_name', 'venue_sub_region_name']
    list_filter = ['venue_sub_region_name']