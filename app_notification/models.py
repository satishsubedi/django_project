from django.db import models
from django.contrib.auth import get_user_model
UserModel = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
       ("doctor","doctor"),
       ("examiner","examiner"),
       ("patient","patient"),
       ("other","other") 
    )
    recipient = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='recipient_user')
    sender = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='sender_user')
    message = models.TextField()
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50,choices=NOTIFICATION_TYPES)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Notification to -{},by {}'.format(self.recipient.email,self.sender.email)











