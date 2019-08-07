from django.contrib import admin
from django.db.models import Case, Value, When

from .models import Region, Task, SubRegion, Theater, Reminder
# Register your models here.

def mark_dropped(modeladmin, request, queryset):
    queryset.update(dropped=Case(When(dropped=False, then=Value(True)), default=Value(False)))

mark_dropped.short_description = "Toggle Dropped"


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'alias']
    search_fields = ['name', 'alias']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie_name', 'city', 'movie_language', 'movie_dimension',
                    'movie_date', 'task_completed', 'search_count', 'dropped']
    fields = ['user', 'movie_name', ('city', 'movie_language', 'movie_dimension'),
              'movie_date', ('task_completed', 'dropped'), 'search_count']
    search_fields = ['user__username', 'movie_name']
    list_filter = ['movie_language', 'movie_dimension', 'task_completed', 'dropped']
    autocomplete_fields = ['city']
    actions = [mark_dropped]

@admin.register(SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
    list_display = ['region', 'subregion_code', 'subregion_name']
    search_fields = ['region__name', 'region__code', 'subregion_code', 'subregion_name']
    list_filter = ['subregion_name']

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue_code', 'subregion']
    list_filter = ['subregion__region']
    search_fields = ['name', 'venue_code']

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'venues', 'language', 'dimension',
                    'date', 'completed', 'dropped', 'found_time']
    fields = ['user', 'name', 'venues', ('language', 'dimension'),
              'date', ('completed', 'dropped'), 'found_time']
    search_fields = ['user__username', 'name']
    list_filter = ['language', 'dimension', 'completed', 'dropped']
