# Generated by Django 2.2 on 2020-05-20 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]