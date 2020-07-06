from rest_framework import serializers,exceptions
from patient.models import PatientCheckupInfo,Finding,PatientHistory,Income,PatientTransaction,PatientInformation
from hospital.models import Hospital,ExaminationType
from authentication.api.serializers import ProfileSerializer

class PatientAppointmentSerializer(serializers.ModelSerializer):
    hospital_id = serializers.IntegerField()

    class Meta:
        model = PatientCheckupInfo
        fields = ('hospital_id','test_type','details')

class PatientAppointmentListSerializer(serializers.ModelSerializer):
    cpt_code=serializers.SerializerMethodField()
    phone=serializers.SerializerMethodField()
    class Meta:
        model = PatientCheckupInfo
        fields=('id','test_type','details','phone','cpt_code')
    def get_phone(self,obj:PatientCheckupInfo):
        if obj.patient:
            return obj.patient.phone
        else:
            return None
    def get_cpt_code(self,obj:PatientCheckupInfo):
        
        test=obj.test_type.all()
        for t in test:
            return t.cpt_code
class PatientAppointmentUpdateSerializer(serializers.ModelSerializer):
    result=serializers.ListField()
    class Meta:
        model=PatientCheckupInfo
        fields=('id','result')
        

class FindingSerializer(serializers.ModelSerializer):
    doctor = serializers.IntegerField(required=False)
    class Meta:
        model = Finding
        fields = ('patient_check_info','doctor','status','remarks')

class PatientVisitAppointmentSerializer(serializers.ModelSerializer):
    hospital_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    class Meta:
        model = PatientCheckupInfo
        fields=('patient_id','hospital_id','test_type','details')
class PatientHistoryCreateSerializer(serializers.ModelSerializer):
  #  patient=ProfileSerializer()
    class Meta:
        model=PatientHistory
        fields=('patient_file','details',)

class PatientTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientTransaction
        fields=('lab_item',)
class PatientTransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientTransaction
        fields=('paid',)

class PatientHistoryListSerializer(serializers.ModelSerializer):
    patient=ProfileSerializer() # nested serializer
    hospital = serializers.SerializerMethodField()
    class Meta:
        model=PatientHistory
        fields=('patient_file','details','patient','hospital')
    def get_hospital(self,obj:Hospital):
        hospital=obj.objects.get(id=1)
        hospital_data={
            "name":hospital.name,
            "address":hospital.address
        }
        return hospital_data
class FindingExportSerializer(serializers.ModelSerializer):
    Details=serializers.SerializerMethodField()
    patient=serializers.SerializerMethodField()
    doctor=serializers.SerializerMethodField()
    # test_type=serializers.SerializerMethodField()
    # total=serializers.SerializerMethodField()
    class Meta:
        model = Finding
        fields=('Details','patient','doctor','status','remarks')
    def get_Details(self,obj:Finding):
        return obj.patient_check_info.details
    def get_patient(self,obj:Finding):
        return obj.patient_check_info.patient
    # def get_test_type(self,obj:Finding):
    #     a=obj.patient_check_info
    #     # return obj.patient_check_info.test_type
    #     return ExaminationType.objects.get(patient_checkup_info=a).test_type
    def get_doctor(self,obj):
        if obj.doctor:
            return obj.doctor.user
        else:
            return None
    # def get_total(self,obj:Finding):
    #     a=obj.patient_check_info
    #     print(a)
    #     return Income.objects.get(patient_checkup_info=a).total
class PatientTransactionExportSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    lab_item=serializers.SerializerMethodField()
    created_date=serializers.SerializerMethodField()
    class Meta:
        model = PatientTransaction
        fields=('id','user','lab_item','total','vat','grandtotal','created_date')
    def get_user(self,obj:PatientTransaction):
        return obj.patient_trxn_user.get_full_name
    def get_lab_item(self,obj:PatientTransaction):
        return obj.lab_item 
    def get_created_date(self,obj:PatientTransaction):
        return obj.created_date

class PatientReportSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    lab_item=serializers.SerializerMethodField()
    created_date=serializers.SerializerMethodField()
    class Meta:
        model = PatientCheckupInfo
        fields=('id','user','lab_item','created_date',)
    def get_user(self,obj:PatientCheckupInfo):
        return obj.patient.get_full_name
    def get_lab_item(self,obj: PatientCheckupInfo):
        return obj.test_type 
    def get_created_date(self,obj: PatientCheckupInfo):
        return obj.date

class PatientTransactionListSerializer(serializers.ModelSerializer):
    patient_trxn_user=ProfileSerializer()
    class Meta:
        model=PatientTransaction
        fields=('id','patient_trxn_user','lab_item','lab_rate','total','vat','grandtotal')

class PatientInformationCreateSerializer(serializers.ModelSerializer):
    middle_name=serializers.CharField(required=False)
    class Meta:
        model=PatientInformation
        fields=('first_name','middle_name','last_name','address','phone','age','sex','tests')
       

