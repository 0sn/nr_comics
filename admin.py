from django.contrib import admin
from models import Comic

class ComicAdmin(admin.ModelAdmin):
    list_display = ('title','date','sequence', 'is_public',)
    search_fields = ['title', 'transcript', 'newstitle', 'news']
    date_hierarchy = 'date'
    ordering = ['-sequence']
    fieldsets = (
        (None, {'fields': ('date','title','comic')}),
        ("Transcription", {'fields':('transcript',)}),
        ("News", {'fields':('newstitle', 'news')}),
        ("Suggestion", {'fields': ('origin',), 'classes': ('collapse','wide',),}),
    )
    filter_vertical = ('origin',)
    
admin.site.register(Comic,ComicAdmin)

