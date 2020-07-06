from rest_framework.generics import ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import Notification
from .serializers import NotificationListSerializer,NotificationDeleteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

class NotificationListView(ListAPIView):
    permission_classes =[IsAuthenticated]
   # queryset =Notification.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['read']
    serializer_class = NotificationListSerializer
    def get_queryset(self):
        user=self.request.user
        return Notification.objects.filter(recipient=user)

class NotificationListCounterView(ListAPIView):
     permission_classes =[IsAuthenticated]
     def get(self,request,*args,**kwargs):         
         user=self.request.user
         notification_obj=Notification.objects.filter(recipient=user,read=False)         
         serializer=NotificationListSerializer(notification_obj,many=True)
         data=serializer.data
         a=len(data)
         data.append({'counter':a})     
         return Response(data)

class NotificationReadAPIView(UpdateAPIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,*args,**kwargs):
        notification_id=self.kwargs['pk']
        user= request.user
        try:
            notification_obj=Notification.objects.get(recipient=user,id=notification_id)
            notification_obj.read=True
            notification_obj.save()
        except:
            raise NotFound("Notification not found")
        return Response({'success':'Notification marked as read'})
class NotificationRetrieveAPIView(RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        queryset=Notification.objects.filter(recipient=request.user,read=False)
        for notification_read in queryset:
            notification_read.read=True
            notification_read.save()
        return Response({'success':'All notification is read'})
class NotificationBulkDelteAPIView(DestroyAPIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,*args,**kwargs):
        queryset=Notification.objects.filter(recipient=request.user,read=False)
        for notification_read in queryset:
            notification_read.delete()
        return Response({'detail':'Deleted sucessfully'})

class NotificationDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer=NotificationDeleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            notification_list=serializer.validated_data['notification_ids']
            for ids in notification_list:
                print(ids)
                try:
                    k=Notification.objects.get(id=ids)
                    print(k)
                except:
                    raise NotFound("selected notification ids not found")
                user=request.user
                if user==k.recipient:
                    k.delete()
                else:
                    raise PermissionDenied({"detail":'you have no permission to delete'})
            return Response({'success':'selected notification deleted'})





        
