import django_filters
from hospital.models import Hospital
class HospitalFilter(django_filters.FilterSet):
    class Meta:
        model = Hospital
        fields = ('is_active',)