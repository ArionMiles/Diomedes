from django.contrib import admin
from .models import Region, Task, SubRegion, Cinemas
# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'alias']
    search_fields = ['name', 'alias']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['username', 'city', 'movie_name', 'movie_language', 'movie_dimension',
                    'movie_date', 'movie_found', 'task_completed', 'notified']
    search_fields = ['username', 'movie_name']
    list_filter = ['movie_language', 'movie_dimension', 'movie_found', 'task_completed', 'notified']
    autocomplete_fields = ['city']

@admin.register(SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
    list_display = ['region_code', 'sub_region_code', 'sub_region_name']
    search_fields = ['sub_region_name']
    # list_filter = ['region_code']

@admin.register(Cinemas)
class CinemasAdmin(admin.ModelAdmin):
    list_display = ['venue_code', 'venue_name', 'venue_sub_region_code', 'venue_sub_region_name']
    search_fields = ['venue_name', 'venue_sub_region_name']
    list_filter = ['venue_sub_region_name']