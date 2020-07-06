from rest_framework.views import APIView
from.serializers import  (PatientAppointmentSerializer,FindingSerializer,PatientVisitAppointmentSerializer,PatientHistoryCreateSerializer,
 PatientHistoryListSerializer,FindingExportSerializer,PatientAppointmentListSerializer,PatientTransactionCreateSerializer,
 PatientInformationCreateSerializer,PatientTransactionUpdateSerializer,PatientTransactionExportSerializer,
 PatientTransactionListSerializer,PatientAppointmentUpdateSerializer,PatientReportSerializer)
from rest_framework.permissions import IsAuthenticated,AllowAny
from hospital.models import Hospital,ExaminationType
from patient.models import PatientCheckupInfo,Finding,Income,PatientHistory,PatientTransaction,PatientInformation
from users.models import Examiner,Doctor,Patient
from app_notification.models import Notification
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.exceptions import NotFound
from django.template.loader import render_to_string
import json
from utils import emailing
from django.views.generic import View
from utils.render_to_pdf import render_to_pdf
from django.contrib .auth import get_user_model
from django.http import FileResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from rest_framework import status
import csv
import io
import barcode
from barcode.writer import ImageWriter
from django.template.loader import get_template
from datetime import datetime
from base64 import b64encode
UserModel=get_user_model()
class PatientAppointmentView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer = PatientAppointmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            hospital = Hospital.objects.get(id=serializer.validated_data['hospital_id'])
            details = serializer.validated_data['details']
            examination_type = serializer.validated_data['test_type']
            # amount = 0
            if request.user.user_type=='patient':
                appointment_obj = PatientCheckupInfo.objects.create(patient=request.user,hospital=hospital,details=details)
                appointment_obj.test_type.set(examination_type)
                appointment_obj.save()
                data = serializer.data
                examiner = Examiner.objects.filter(hospital=hospital,is_active=True)
                for examiner_obj in examiner:
                    Notification.objects.create(recipient=examiner_obj.user,sender=request.user,message=appointment_obj.details,notification_type='examiner')
                return Response(data=data)
            return Response("permission denied")
# class PatientAppointmentUpdateView(UpdateAPIView):
#     permission_classes=[IsAuthenticated]
#     queryset = PatientCheckupInfo.objects.all()
#     serializer_class = PatientAppointmentUpdateSerializer
#     def patch(self, request, *args, **kwargs):
#          patient_obj = self.kwargs['pk']
#          if request.result.id == patient_obj:
#              return self.partial_update(request,*args,**kwargs)
#          return Response({'detail': 'you donot have permission to update the profile'},
#                         status=status.HTTP_400_BAD_REQUEST)
class  PatientAppointmentUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,*args,**kwargs):
        serializer=PatientAppointmentUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            result=serializer.validated_data.get('result')
            if request.user.user_type=='examiner':
                patient_obj=self.kwargs['pk']
                results=[]
                pa=PatientCheckupInfo.objects.get(is_examined=False,id=patient_obj)
                for ra in result:
                    results.append(ra)
                pa.result=results
                pa.is_examined=True
                pa.is_active=False
                pa.save()
            return Response({'detail':'you are not authorized'})
                
class PatientTransactionCreateView(APIView): 
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer=PatientTransactionCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            test_type= serializer.validated_data['lab_item']
            total=serializer.validated_data['total']
            if request.user.user_type=="patient":
                patienttransaction_obj=PatientTransaction.objects.create(patient_trxn_user=request.user)
                patienttransaction_obj.lab_item.set(test_type)
                data=serializer.data
                total=0
                for lab_item in test_type:
                    lab_item_obj=ExaminationType.objects.get(id=lab_item.id)
                    rate=lab_item_obj.rate
                    total +=rate
                vat=total*0.13
                grandtotal=vat+total
                patienttransaction_obj.total=total
                patienttransaction_obj.vat=vat
                patienttransaction_obj.grandtotal=grandtotal
                patienttransaction_obj.save()
                # if patienttransaction_obj.paid :
                #     Income.objects.create(patient_trxn=patienttransaction_obj,total=grandtotal)
                return Response(data)
            return Response("Permission Denied")
class PatientTransactionListView(ListAPIView):
        permission_classes=[IsAuthenticated]
        def get(self,request,*args,**kwargs):
            trn_id=self.kwargs['pk']
            patient_trn_obj=PatientTransaction.objects.get(id=trn_id)
            queryset=PatientTransaction.objects.filter(id=patient_trn_obj.id)
            serializer=PatientTransactionListSerializer(queryset,many=True)
            data=serializer.data
            return Response(data)

class PatientTransactionUpdateAPIView(UpdateAPIView):
     permission_classes = (IsAuthenticated,)    
     serializer_class = PatientTransactionUpdateSerializer
     def put(self, request, *args, **kwargs):    
        trxn_obj = self.kwargs['pk']
        patient_trxn_obj=PatientTransaction.objects.get(id=trxn_obj)
        user=patient_trxn_obj
        patient_trxn_obj.paid=True
        grandtotal=patient_trxn_obj.grandtotal
        patient_trxn_obj.save()
        if patient_trxn_obj.paid:
            Income.objects.create(patient_trxn=user,total=grandtotal)
        return Response({'detail': 'sucessfully updated'})

class PatientAppointmentList(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=PatientAppointmentListSerializer
    def get_serializer(self,queryset):
        return self.serializer_class(queryset)
    def get(self,request,*args,**kwargs):
        user=request.user
        if user.user_type=='examiner':
           patient_checkup_info_id= self.kwargs['pk']
           patient_checkup_info_id=PatientCheckupInfo.objects.get(id=patient_checkup_info_id,is_examined=False,is_active=True)
           x=json.loads(patient_checkup_info_id.result)
           serializer=self.get_serializer(patient_checkup_info_id)
           data=serializer.data
           data['results']=x
        #    serializer = PatientAppointmentListSerializer(queryset,many=True)
           return Response(data)
        else:
            return Response({'detail':'You dont have permission '})

class FindingView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer = FindingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            patient_checkup_form = serializer.validated_data['patient_check_info'] 
            try:
                patient_checkup_obj = PatientCheckupInfo.objects.get(id=patient_checkup_form.id,is_active=True)
            except PatientCheckupInfo.DoesNotExist:
                raise NotFound("Doctor is not found")
            status = serializer.validated_data['status']
            remarks = serializer.validated_data['remarks']
            #doctor = serializer.validated_data.get('doctor')
            doctor = serializer.validated_data.get('doctor')
            if request.user.user_type =='examiner':
                if doctor:
                    try:
                        doctor=Doctor.objects.get(id=doctor)
                    except Doctor.DoesNotExist:
                        raise NotFound("Doctor is not found")
                    try:
                        doctor_obj=UserModel.objects.get(email=doctor.user.email)
                    except UserModel.DoesNotExist:
                        raise NotFound("Doctor email is not found")
                    patient_checkup_obj.is_active = True
                    Finding.objects.create(patient_check_info=patient_checkup_obj,status=status,remarks=remarks,doctor=doctor)
                    Notification.objects.create(recipient=doctor_obj,sender=request.user,message="new checkup request",notification_type='doctor')
                    Notification.objects.create(recipient=patient_checkup_obj.patient,sender=request.user,message="checkup_undergoing",notification_type='patient')
                    doc_context={
                            'user':doctor_obj.email,
                            'domain':'127.0.0.1:8000',
                            'patient':patient_checkup_obj.patient.email,
                            'test':patient_checkup_obj.test_type.all(),
                            'details':patient_checkup_obj.details
                            }
                    patient_context={
                        'user':patient_checkup_obj.patient.email,
                        'doctor':doctor_obj.email,
                        'test':patient_checkup_obj.test_type.all(),
                        'details':patient_checkup_obj.details
                    }
                    mail_subject=' Checkup request'
                    message= render_to_string('doctor.html',doc_context)
                    email_plaintext_message= render_to_string('doctor.txt',doc_context)
                    to_email=doctor_obj.email
                    success= emailing.EmailThread(mail_subject,message,doc_context,[doctor_obj.email,]).start()
                    message2= render_to_string('patient.html',patient_context)
                    email_plaintext_message= render_to_string('patient.txt',patient_context)
                    success= emailing.EmailThread(mail_subject,message2,patient_context,[patient_checkup_obj.patient.email,]).start()
                else:
                    Finding.objects.create(patient_check_info=patient_checkup_obj,status=status,remarks=remarks)
                    patient_checkup_obj.is_active = False
                    Notification.objects.create(recipient=patient_checkup_obj.patient,sender=request.user,message="checkup_completed",notification_type='patient')
                patient_checkup_obj.is_examined =True
                patient_checkup_obj.examiner = request.user
                patient_checkup_obj.save()
                return Response(serializer.data)
            return Response('Permission Denied')
class PatientVisitAppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer = PatientVisitAppointmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                hospital = Hospital.objects.get(id=serializer.validated_data['hospital_id'])
            except Hospital.DoesNotExist:
                raise NotFound("Hospital is not found")
            try:
                patient = UserModel.objects.get(id=serializer.validated_data['patient_id'])
            except UserModel.DoesNotExist:
                raise NotFound("patient not found")
            examination_type = serializer.validated_data['test_type']
            details = serializer.validated_data['details']
            amount=0
            if request.user.user_type=='examiner':
                visitappointment_obj=PatientCheckupInfo.objects.create(patient=patient,hospital=hospital,examiner=request.user,details=details)
                visitappointment_obj.test_type.set(examination_type)
                for test_type in examination_type:
                    patientvisitappointment_obj=ExaminationType.objects.get(name=test_type)
                    amount+=patientvisitappointment_obj.rate
                amount = amount+amount*0.13
                Income.objects.create(patient_checkup_info=visitappointment_obj,total=amount)
                data=serializer.data
                data['amount']=amount
                Notification.objects.create(recipient=patient,sender=request.user,message=details,notification_type='patient')
                return Response(data=data)
            return Response("permission Denied")
            
class PatientHistoryCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer=PatientHistoryCreateSerializer(data=request.data)
        user=request.user
        if user.user_type=='patient':  
            if serializer.is_valid(raise_exception=True):
                history=serializer.validated_data['patient_file']
                details=serializer.validated_data['details']
                PatientHistory.objects.create(patient=user,patient_file=history,details=details)
                return Response({'detail':"Patient history created succesfully"})
        else:
            return Response({"detail":'You dont have permission to upload the file'})
class PatientHistoryListAPIView(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=PatientHistoryCreateSerializer
    def get_queryset(self):
        return PatientHistory.objects.filter(patient=self.request.user)

class PatientHistoryList(ListAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        user=request.user
        if user.user_type=='examiner':
           patient_id= self.kwargs['pk']
           patient_id=UserModel.objects.get(id=patient_id)
           queryset=PatientHistory.objects.filter(patient__id=patient_id.id)
           serializer = PatientHistoryListSerializer(queryset,many=True)
           return Response(serializer.data)
        else:
            return Response({'detail':'You dont have permission '})
class PatientHistoryDelete(DestroyAPIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,*args,**kwargs):
        user=request.user
        if user.user_type=="patient":
            patient_obj=PatientHistory.objects.filter(patient=user)
            for obj in patient_obj:
                obj.delete()
            return Response({'detail':'Patient History delted successfully'})
        else:
            return Response("Permission denied")

class PatientHistoryRetrieve(RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        history_id = self.kwargs['pk']
        user=request.user
        if user.user_type=='patient':
            try:
                 patient_history_obj=PatientHistory.objects.get(id=history_id)
            except:
                raise NotFound("patient history not found")         
            serializer=PatientHistoryListSerializer(patient_history_obj)
            return Response(serializer.data)
        else:
            return Response({'detail':'You dont have permission'})

class FindingExportCSVView(APIView):
    permission_classes=[AllowAny]
    serializer_class=FindingExportSerializer
    def get_serializer(self,queryset):
        return self.serializer_class(queryset)
    def get (self,request,*args,**kwargs):
        id = self.kwargs['pk']
        finding_obj=Finding.objects.get(id=id)
        serializer=self.get_serializer(finding_obj)
        data=serializer.data
        data['id']=id
        # html = template.render(data)
        pdf = render_to_pdf('invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

        # def  fileToImageBase64Url(file: File): 
        #     const blob = new Blob([file], { type: 'image/png' })
        #     return URL.createObjectURL(blob)

class PatientTransactionExportView(APIView):
    permission_classes=[AllowAny]
    serializer_class=PatientTransactionExportSerializer
    def get_serializer(self,queryset):
        return self.serializer_class(queryset)
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        id=str(id)
        print(id)
        patient_trxn_obj=PatientTransaction.objects.get(id=id)
        barCodeImage = barcode.get('Code128', id, writer=ImageWriter())
        file = barCodeImage.save(barCodeImage)
        bytes = file.encode(encoding='UTF-8')
        encoded=b64encode(bytes)
        mime = "image/png"
        uri = "data:%s;base64,%s" % (mime, encoded)
        print(uri)
        serializer=self.get_serializer(patient_trxn_obj)
        data=serializer.data
        data['url']=uri
        pdf=render_to_pdf('billing.html',data)
        return HttpResponse(pdf,content_type='application/pdf')

class PatientReportExportView(APIView):
    permission_classes=[AllowAny]
    serializer_class=PatientReportSerializer
    def get_serializer(self,queryset):
        return self.serializer_class(queryset)
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        id=str(id)
        patient_trxn_obj=PatientCheckupInfo.objects.get(id=id)
        barCodeImage = barcode.get('Code128', id, writer=ImageWriter())
        file = barCodeImage.save(barCodeImage)
        bytes = file.encode(encoding='UTF-8')
        encoded=b64encode(bytes)
        mime = "image/png"
        uri = "data:%s;base64,%s" % (mime, encoded)
        x=json.loads(patient_trxn_obj.result)
        serializer=self.get_serializer(patient_trxn_obj)
        data=serializer.data      
        data['results']=x
        # data['url']=uri
        pdf=render_to_pdf('report.html',data)
        return HttpResponse(pdf,content_type='application/pdf')

# class FindingExportCSVView(APIView):
#     serializer_class=FindingExportSerializer
#     def get_serializer(self,queryset,many=True):
#         return self.serializer_class(queryset,many=many)
#     def get (self,request,*args,**kwargs):
#         finding_obj=Finding.objects.all()
#         response=HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="test.csv"'
#         serializer=self.get_serializer(finding_obj)
#         header=FindingExportSerializer.Meta.fields
#         writer=csv.DictWriter(response,fieldnames=header)
#         writer.writeheader()
#         data=serializer.data
#         for row in data:
#             writer.writerow(row)
#         return response

class PatientInformationCreate(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer=PatientInformationCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            fname = serializer.validated_data.get('first_name')
            mname = serializer.validated_data.get('middle_name')
            lname = serializer.validated_data.get('last_name')
            address = serializer.validated_data.get('address')
            phone = serializer.validated_data.get('phone')
            age = serializer.validated_data.get('age')
            sex = serializer.validated_data.get('sex')
            test_type = serializer.validated_data.get('tests')
            # test_details = serializer.validated_data('test_details')
            if request.user.user_type=="examiner":
                patient_information_obj= PatientInformation.objects.create(first_name=fname,middel_name=mname,last_name=lname,address=address,phone=phone,age=age,sex=sex,createdby=request.user)
                patient_information_obj.test.set(test_type)
                patient_information_obj.save()
                Notification.objects.create(recipient=request.user,sender=request.user,message="hello",notification_type='examiner')
                data=serializer.data
                return Response (data= data)
            return Response("permission denied")


            

            

            

            

        
       