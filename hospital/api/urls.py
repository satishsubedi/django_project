from django.urls import path
from .views import (HospitalAPIView,HospitalRetrieveUpdateAPIView,HospitalDestroyAPIView,DoctorSpecialityCreateAPIView,
DoctorSpecialityRetrieveUpdateDestroyAPIView,DoctorProfileView,DoctorProfileDetailView,ExaminerProfileView,
ExaminerProfileDetailView,NearbyHospitalListView,ExaminationTypeView,ExaminationTypeListProfile, 
)

urlpatterns = [
    #API Endpoints
    path('create/',HospitalAPIView.as_view(),name='hospital_create'),
    path('list/',HospitalAPIView.as_view(),name='hospital_list'),
    path('delete/<int:pk>/',HospitalDestroyAPIView.as_view(),name='hospital_delete'),
    path('<int:pk>/',HospitalRetrieveUpdateAPIView.as_view(),name='hospital_detail_update'),
    path('listspeciality/',DoctorSpecialityCreateAPIView.as_view(),name='docotorspeciality_list'),
    path('createspeciality/',DoctorSpecialityCreateAPIView.as_view(),name='docotorspeciality_create'),
    path('speciality/<int:pk>/',DoctorSpecialityRetrieveUpdateDestroyAPIView.as_view(),name='docotorspeciality_details'),
    path('doctor/profile/create/',DoctorProfileView.as_view(),name='doctor_profile'),
    path('doctor/profile/detail/',DoctorProfileDetailView.as_view(),name='doctor_profile_detail'),
    path('examiner/profile/create/',ExaminerProfileView.as_view(),name='examiner_profile'),
    path('examiner/profile/detail/',ExaminerProfileDetailView.as_view(),name='examiner_profile_detail'),
    path('nearby/', NearbyHospitalListView.as_view(), name='nearest_hospital_list'),

    path('examinationtype/create/',ExaminationTypeView.as_view(),name='examinationtype_create'),
    path('examinationtype/list/',ExaminationTypeListProfile.as_view(),name='examinationtype_list'),
    #path('examinationtype/update/',ExaminationTypeUpdateProfile.as_view(),name='examinationtype_update'),
   # path('examinationtype/retrieve/<int:pk>/',ExaminationTypeRetrieveProfileView.as_view(),name='examinationtype_retrieve'),



    
    

 
]