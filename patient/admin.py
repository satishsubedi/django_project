from django.contrib import admin
from .models import PatientHistory,PatientCheckupInfo,Finding,Income,PatientTransaction,PatientInformation
from import_export.admin import ImportExportModelAdmin
admin.site.register(PatientTransaction)
admin.site.register(PatientInformation)

class PatientHistoryAdmin(admin.ModelAdmin):
    list_per_page= 10
    list_display = ['id','patient','patient_file','details']
    list_display_links =['id','patient_file']
    list_filter=['details']
    search_fields=['id','patient']
    readonly_fileds=['id']

@admin.register(PatientCheckupInfo)
class PatientCheckupInfoAdmin(ImportExportModelAdmin):
    list_per_page= 10
    list_display = ['id','hospital','is_examined','details','is_active','patient','examiner']
    list_display_links =['id',]
    list_filter=['hospital']
    search_fields=['id','hospital']
    readonly_fileds=['id']
class IncomeAdmin(admin.ModelAdmin):
    list_per_page= 10
    list_display = ['id','patient_trxn','total']
    list_display_links =['id']
    #list_filter=['is_active']
    search_fields=['id']
    readonly_fileds=['id']
admin.site.register(PatientHistory,PatientHistoryAdmin)

admin.site.register(Finding)
admin.site.register(Income,IncomeAdmin)


# Register your models here.
