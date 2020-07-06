from django.urls import path
from .views import (PatientAppointmentView,FindingView,PatientVisitAppointmentView,PatientHistoryCreateAPIView,
PatientHistoryListAPIView,PatientHistoryList,PatientHistoryDelete,PatientHistoryRetrieve,FindingExportCSVView,
PatientAppointmentList,PatientTransactionCreateView,PatientInformationCreate,PatientTransactionUpdateAPIView,
PatientTransactionExportView,PatientTransactionListView,PatientAppointmentUpdateView,PatientReportExportView)

urlpatterns = [
path('appointment/',PatientAppointmentView.as_view(),name='patient_checkup_info'),
path('appointment/update/<int:pk>/',PatientAppointmentUpdateView.as_view(),name='patient_checkup_info_update'),
path('appointment/list/<int:pk>/',PatientAppointmentList.as_view(),name='patient_checkup_info_list'),
path('finding/',FindingView.as_view(),name='patient_finding'),
path('visitappointment/',PatientVisitAppointmentView.as_view(),name='patient_checkup_info_visit'),
path('history/',PatientHistoryCreateAPIView.as_view(),name="patient_history"),
path('history/list/',PatientHistoryListAPIView.as_view(),name="patient_history_list"),
path('history/list/<int:pk>/',PatientHistoryList.as_view(),name="patient_history_list_id"),
path('history/delete/',PatientHistoryDelete.as_view(),name="patient_history_delete"),
path('history/retrieve/<int:pk>/',PatientHistoryRetrieve.as_view(),name="patient_history_retrieve"),
path('findings/export/<int:pk>/',FindingExportCSVView.as_view(),name='finding_export'),
path('transaction/',PatientTransactionCreateView.as_view(),name="patient_transation"),
path('transaction/<int:pk>/',PatientTransactionUpdateAPIView.as_view(),name="patient_transation_update"),
path('information/create/',PatientInformationCreate.as_view(),name="patient_information"),
path('transaction/export/<int:pk>/',PatientTransactionExportView.as_view(),name="patient_transation_export"),
path('transaction/list/<int:pk>/',PatientTransactionListView.as_view(),name="patient_transation_list"),
path('report/export/<int:pk>/',PatientReportExportView.as_view(),name="patient_report_export")

]