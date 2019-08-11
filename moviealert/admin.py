from django.contrib import admin
from django.db.models import Case, Value, When

from .models import Region, SubRegion, Theater, Reminder, Profile
# Register your models here.

def mark_dropped(modeladmin, request, queryset):
    queryset.update(dropped=Case(When(dropped=False, then=Value(True)), default=Value(False)))

mark_dropped.short_description = "Toggle Dropped"


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'alias']
    search_fields = ['name', 'alias']

@admin.register(SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
    list_display = ['region', 'code', 'name']
    search_fields = ['region__name', 'region__code', 'code', 'name']

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'region', 'subregion']
    search_fields = ['name', 'code']

class TheaterInline(admin.TabularInline):
    model = Reminder.theaters.through
    autocomplete_fields = ['theater']

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'language', 'dimension',
                    'date', 'completed', 'dropped']
    fields = ['user', 'name', ('language', 'dimension'),
              'date', ('completed', 'dropped')]
    search_fields = ['user__username', 'name']
    list_filter = ['language', 'dimension', 'completed', 'dropped']
    inlines = [
        TheaterInline,
    ]
    autocomplete_fields = ['theaters', 'user']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'region', 'subregion']
    search_fields = ['user__username', 'region__code', 'subregion__code']
