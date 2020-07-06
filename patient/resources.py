from import_export import resources
from patient.models import PatientCheckupInfo

class PatientResource(resources.ModelResource):
    class Meta:
       model= PatientCheckupInfo
