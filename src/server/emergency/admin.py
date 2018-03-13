from django.contrib import admin
from .models import Entry

class EntryAdmin(admin.ModelAdmin):
    readonly_fields=('generate_MarkerScript',)
    list_display = ('submit_time', 'address', 'emergency_type')
    fields=(('submit_time','emergency_type'),'original_email','suspect_name',
            'address','generate_MarkerScript','marker_script','suspect_traits',
            'time','image_url','optional_info')

    class Media:
        js=('../index_files/jquery-1.11.0.min.js.download',)
# Register your models here.
admin.site.register(Entry, EntryAdmin)
