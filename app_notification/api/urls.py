from django.urls import path
from .views import NotificationListView,NotificationReadAPIView,NotificationRetrieveAPIView,NotificationBulkDelteAPIView,NotificationDeleteAPIView,NotificationListCounterView
urlpatterns=[
    path('list/',NotificationListView.as_view(),name='notification'),
    path('listcounter/',NotificationListCounterView.as_view(),name='notificationcounter'),

    path('read/<int:pk>/',NotificationReadAPIView.as_view(),name='notification_read'),
    path('read/all/',NotificationRetrieveAPIView.as_view(),name='notification_read_all'),
    path('delete/all/',NotificationBulkDelteAPIView.as_view(),name='notification_delete_all'),
    path('delete/',NotificationDeleteAPIView.as_view(),name='notification_delete')
]