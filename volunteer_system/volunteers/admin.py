from django.contrib import admin
from .models import Activity, Volunteer

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'location', 'description')
    ordering = ('-date',)

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'activity', 'notes', 'created_at')
    list_filter = ('activity',)
    search_fields = ('name', 'phone', 'notes')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Volunteer, VolunteerAdmin)