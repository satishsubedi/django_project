from rest_framework import serializers,exceptions
from hospital.models import Hospital,ExaminationType,PatientCheckupResult
from users.models import DoctorSpeciality,Doctor,Examiner
from authentication.api.serializers import ProfileSerializer




class HospitalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id', 'created_by', 'name', 'latitude', 'longitude', 'address', 'image', 'description', 'is_active')
        read_only_fields = ('id','created_by','is_active')

class HospitalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class HospitalRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('name', 'latitude', 'longitude', 'address', 'description', 'image','is_active')

class DoctorSpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSpeciality
        fields = ('name','is_active')

class DoctorSpecialityRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSpeciality
        fields = '__all__'
        read_only_fields = ('id',)

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields=('license_id','speciality','degree','hospital')

class DoctorProfileSerializer(serializers.ModelSerializer):
    user=ProfileSerializer()
    speciality=DoctorSpecialityRetrieveUpdateSerializer(many=True)
    hospital=HospitalListSerializer(many=True)
    class Meta:
        model=Doctor
        fields=('user','license_id','speciality','degree','hospital')

class ExaminerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Examiner
        fields=('license_id','lab_details','degree','hospital')

class ExaminerProfileSerializer(serializers.ModelSerializer):
    user=ProfileSerializer()
    hospital=HospitalListSerializer(many=True)
    class Meta:
        model=Examiner
        fields=('user','license_id','lab_details','degree','hospital')

class NearbyHospitalSerializer(serializers.Serializer):
    latitude=serializers.FloatField(required=True,min_value=-90,max_value=90)
    longitude=serializers.FloatField(required=True,min_value=-180,max_value=180)

class ExaminationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExaminationType
        fields = ('id','name','rate')
class ExaminationTypeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExaminationType
        fields = ('id','name','status','rate',)
        read_only_fields =('status',)
class PatientCheckupResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientCheckupResult
        fields=('id','value')






