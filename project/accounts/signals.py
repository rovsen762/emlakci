from .models import Account, AccountCustomers,Balance
from django.db.models.signals import post_save
from django.dispatch import receiver    


# create balance when Account is created
@receiver(post_save, sender=Account)
def create_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(account=instance)    