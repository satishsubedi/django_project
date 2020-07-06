from rest_framework.generics import( ListCreateAPIView,RetrieveUpdateAPIView,DestroyAPIView,
RetrieveUpdateDestroyAPIView,RetrieveAPIView,ListAPIView,UpdateAPIView)
from rest_framework.views import APIView
from .serializers import (HospitalCreateSerializer,HospitalListSerializer,HospitalRetrieveUpdateSerializer,DoctorSpecialitySerializer,
DoctorSpecialityRetrieveUpdateSerializer,DoctorSerializer,DoctorProfileSerializer,ExaminerSerializer,ExaminationTypeProfileSerializer,
ExaminerProfileSerializer,NearbyHospitalSerializer,ExaminationTypeSerializer,ExaminationTypeProfileSerializer)
from hospital.models import Hospital,ExaminationType
from users.models import DoctorSpeciality,Doctor,Examiner
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import APIException,NotFound
from utils.pagination_utils import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import HospitalFilter
from utils.locationutils import fetch_nearest_hospital_with_location

class HospitalAPIView(ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = HospitalFilter
    
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        return Hospital.objects.all().order_by('-created_time')

class HospitalRetrieveUpdateAPIView(RetrieveUpdateAPIView):
     serializer_class = HospitalRetrieveUpdateSerializer
     lookup_url_kwarg = 'pk'
     permission_classes = [IsAuthenticated]
     queryset = Hospital.objects.all()

class HospitalDestroyAPIView(DestroyAPIView):
    serializer_class = HospitalRetrieveUpdateSerializer
    #lookup_url_kwarg = 'pk'
    def delete(self,*args,**kwargs):
        hospital_id = self.kwargs['pk']
        try:
            hospital = Hospital.objects.get(id=hospital_id)
            hospital.delete()
            return Response({'detail':'Deleted Sucessfully'})
        except Hospital.DoesNotExist:
            raise NotFound("Hospital with the provided id not found")


class DoctorSpecialityCreateAPIView(ListCreateAPIView):
    serializer_class = DoctorSpecialitySerializer
    permission_classes = [AllowAny]
    queryset = DoctorSpeciality.objects.all()

    #def perform_create(self,serializer):
      #  serializer.save()
    
    def get_queryset(self):
        return DoctorSpeciality.objects.filter(is_active=True)

class DoctorSpecialityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSpecialityRetrieveUpdateSerializer
    lookup_url_kwarg = 'pk'
    permission_classes =[AllowAny]
    queryset = DoctorSpeciality.objects.all()

    def get_queryset(self):
        return DoctorSpeciality.objects.all()

class DoctorProfileView(APIView):
    permission_class=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        serializer=DoctorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=request.user
            if user.user_type=='doctor':
                license_id=serializer.validated_data['license_id']
                speciality=serializer.validated_data['speciality']
                hospitals=serializer.validated_data['hospital']
                degree=serializer.validated_data['degree']
                doctor_profile=Doctor.objects.create(user=user,license_id=license_id,degree=degree)
                doctor_profile.speciality.set(speciality) #set is for ManyToMany Field
                doctor_profile.hospital.set(hospitals)
                return Response({'detail':'Doctor Profile Created Succesfully'})
            else:
                return Response({'detail':'You do not have permission to create Doctor Profile.'})

class DoctorProfileDetailView(RetrieveAPIView):
    permission_class=(IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        user=request.user
        if user.user_type=='doctor':
            try:
                user = Doctor.objects.get(user__id=user.id)
                serializer = DoctorProfileSerializer(user)
                return Response(serializer.data)
            except Doctor.DoesNotExist:
                raise NotFound("Doctor Profile Not Found")
        else:
            return Response({'detail':'You do not have Permission'})

class ExaminerProfileView(APIView):
    permission_class=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        serializer=ExaminerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=request.user
            if user.user_type=='examiner':
                license_id=serializer.validated_data['license_id']
                lab_details=serializer.validated_data['lab_details']
                hospitals=serializer.validated_data['hospital']
                degree=serializer.validated_data['degree']
                examiner_obj=Examiner.objects.filter(user=user)
             #   print(examiner_obj)
                if examiner_obj:
                    raise APIException("user already is examiner user")
                else:
                    examiner_profile=Examiner.objects.create(user=user,license_id=license_id,degree=degree,lab_details=lab_details)
                    examiner_profile.hospital.set(hospitals)
                  #  return Response({'detail':'Examiner Profile Created Succesfully'})
                    return Response(serializer.data)
            else:
                return Response({'detail':'You do not have permission to create Doctor Profile.'})

class ExaminerProfileDetailView(RetrieveAPIView):
    permission_class=(IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        user=request.user
        if user.user_type=='examiner':
            try:
                user = Examiner.objects.get(user__id=user.id)
                serializer = ExaminerProfileSerializer(user)
                return Response(serializer.data)
            except Examiner.DoesNotExist:
                raise NotFound('Examiner Profile Not Found')
        else:
            return Response({'detail':'You do not have Permission'})

class NearbyHospitalListView(ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Hospital.objects.all()
    def post(self,request,*args,**kwargs):
        serializer = NearbyHospitalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_latitude = serializer.validated_data['latitude']
            user_longitude = serializer.validated_data['longitude']
            hospitals=[]
            hospital_list = Hospital.objects.all()
            for hospital_obj in hospital_list:
                hospitals.append(hospital_obj)
            nearest_hospital = fetch_nearest_hospital_with_location(hospitals,user_latitude,user_longitude)
            return Response({'detail':nearest_hospital,'success':'Nearby hospital fetched sucessfully'})

class ExaminationTypeView(APIView):
    permissions_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer = ExaminationTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            if user.user_type=='examiner':
                name = serializer.validated_data['name']
                rate = serializer.validated_data['rate']
                examinationtype_obj = ExaminationType.objects.filter(name=name)
                if examinationtype_obj:
                    raise APIException("Provided name is already available")
                else:
                    examinationtype_profile = ExaminationType.objects.create(name=name,rate=rate)
                    examinationtype_profile.save()
                    return Response(serializer.data)
            else:
                return Response({'detail':'You do not have permission to create examination type'})

class ExaminationTypeListProfile(ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset = ExaminationType.objects.all()
    serializer_class = ExaminationTypeProfileSerializer
   
        



