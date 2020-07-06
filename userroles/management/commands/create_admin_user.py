from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db import transaction
UserModel = get_user_model()

class Command(BaseCommand):
    help ="Admin user created"
    def handle(self, *args, **options):
        group,created = Group.objects.get_or_create(name="Super Admin")
        with transaction.atomic():
            user = UserModel.objects.create_user('admin@admin.com','admin123')
            user.is_staff=True
            user.is_superuser =True
            user.groups.add(group)
            user.save()
        self.stdout.write("Admin user created sucessfully")