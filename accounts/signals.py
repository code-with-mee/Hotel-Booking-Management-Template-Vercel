from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomerProfile


@receiver(post_save, sender=User)
def ensure_customer_profile(sender, instance, created, **kwargs):
    """Make sure every user has a CustomerProfile.

    Registration fills in the real details afterwards via the form, but
    users created another way (createsuperuser, the admin panel) also get
    a profile so booking/review views never hit RelatedObjectDoesNotExist.
    """
    if created:
        CustomerProfile.objects.get_or_create(
            user=instance,
            defaults={
                'full_name': instance.get_full_name() or instance.username,
                'phone': '',
                'address': '',
            },
        )
