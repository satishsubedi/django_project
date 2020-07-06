from django.db import models
from users.models import Patient,Doctor
from hospital.models import ExaminationType,Hospital,PatientCheckupResult
from django.contrib.auth import get_user_model
from users.models import PortalUser


UserModel = get_user_model()


class PatientHistory(models.Model):
    patient = models.ForeignKey(PortalUser,on_delete=models.CASCADE,related_name='patient_history')
    patient_file = models.FileField(null=True,blank=True,upload_to='media/files/patient/%Y-%m-%d/')
    details = models.TextField()

    def __str__(self):
        return self.patient.email

class PatientCheckupInfo(models.Model):
    patient = models.ForeignKey(PortalUser,on_delete=models.CASCADE,related_name='patient_user')
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE,related_name='hospital_appointment')
    test_type = models.ManyToManyField(ExaminationType)
    result=models.TextField()
    examiner = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='patient_examiner',null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_examined = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    details = models.TextField()


    def __str__(self):
        return self.patient.email
class Finding(models.Model):
    patient_check_info = models.ForeignKey(PatientCheckupInfo,on_delete=models.CASCADE,related_name='findings')
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='assigned_doctor',null=True,blank=True)
    status = models.BooleanField(default=True)
    remarks = models.TextField()
    # created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_check_info.patient.email

class PatientTransaction(models.Model):
    PAID_TYPES = (
       ("online","online"),
       ("cash","cash"),
       ("other","other") 
    )
    patient_trxn_user=models.ForeignKey(PortalUser,on_delete=models.CASCADE,related_name='patient_trxn_user')
    lab_item=models.ManyToManyField(ExaminationType,related_name='lab_item')
    total=models.FloatField(null=True,blank=True)
    vat=models.FloatField(null=True,blank=True)
    grandtotal=models.FloatField(null=True,blank=True)
    paidby=models.CharField(max_length=50,choices=PAID_TYPES)
    created_date = models.DateTimeField(auto_now_add=True)
    paid=models.BooleanField(default=False,verbose_name='Paid')
    
    def __str__(self):
        return self.patient_trxn_user.email
   

class Income(models.Model):
    patient_trxn=models.ForeignKey(PatientTransaction,on_delete=models.CASCADE,related_name='transaction')
    total=models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_trxn.patient_trxn_user.email



class PatientInformation(models.Model):
    SEX_TYPES=(
    ('male','male'),
    ('female','female')
    )
    first_name=models.CharField(max_length=50)
    middel_name=models.CharField(max_length=50,null=True,blank=True)
    last_name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=50)
    age=models.CharField(max_length=10)
    sex=models.CharField(max_length=10,choices=SEX_TYPES)
    createdby=models.ForeignKey(PortalUser,on_delete=models.CASCADE,related_name='created_user')
    test =models.ManyToManyField(ExaminationType)
    testdetails=models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    examiner_finding=models.TextField()
    doctor_recommendation=models.TextField()

    def __str__(self):
        return self.first_name


    
    













