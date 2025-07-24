# bussapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vehicle_list
import logging

@receiver(post_save, sender=Vehicle_list)
def vehicle_added_signal(sender, instance, created, **kwargs):
    if created:
        # You can replace this with sending an email, audit log, or a notification
        print(f"🚗 New vehicle added: {instance.Add_vehicle_numbers}")
