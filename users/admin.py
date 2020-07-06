from django.contrib import admin
from .models import Patient,DoctorSpeciality,Doctor,Examiner,PortalUser

class DoctorAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','license_id','degree']
    list_filter=['is_active']
    search_fields=['is_active']
    readonly_fields=('id',)
class DoctorSpecialityAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','name']
    list_filter=['is_active']
    search_fields=['is_active']
    readonly_fields=('id',)
class ExaminerAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','license_id','lab_details','degree']
    list_filter=['is_active']
    search_fields=['is_active']
    readonly_fields=('id',)
class PatientAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','user']
    list_filter=['is_active']
    search_fields=['is_active']
    readonly_fields=('id',)
class PortalUserAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display=['id','email','password','phone','user_type','first_name','last_name','is_active']
    list_filter=['is_active']
    search_fields=['email']
    #readonly_fields=('id','satus','user_type',)

admin.site.register(Doctor,DoctorAdmin)
admin.site.register(DoctorSpeciality,DoctorSpecialityAdmin)
admin.site.register(Examiner,ExaminerAdmin)
admin.site.register(Patient,PatientAdmin)
admin.site.register(PortalUser,PortalUserAdmin)