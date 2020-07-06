from django.contrib import admin
from .models import Hospital,ExaminationType,PatientCheckupResult
admin.site.register(PatientCheckupResult)

class HospitalAdmin(admin.ModelAdmin):
    list_per_page= 10
    list_display = ['id','name','address','is_active']
    list_display_links =['id','name']
    list_filter=['is_active']
    search_fields=['id','name']
    readonly_fileds=['id']
class ExaminationTypeAdmin(admin.ModelAdmin):
    list_per_page= 10
    list_display = ['id','name','rate']
    list_display_links =['id','name','rate']
    list_filter=['name']
    search_fields=['id','name']
    readonly_fileds=['id']

admin.site.register(Hospital,HospitalAdmin)
admin.site.register(ExaminationType,ExaminationTypeAdmin)


# Register your models here.
