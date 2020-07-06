from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','recipient','sender','message','notification_type','read']
    list_filter=['read']
    search_fields=['read']
    readonly_fields=('id',)

admin.site.register(Notification,NotificationAdmin)

# Register your models here.
