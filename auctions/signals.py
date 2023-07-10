from django.db.models.signals import pre_save
from django.dispatch import receiver
from auctions.models import Auction, Category


@receiver(pre_save, sender=Auction)
def create_category(sender, instance, **kwargs):
    category_name = instance.category.name if instance.category else None

    if category_name:
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            category = Category.objects.create(name=category_name)

        instance.category = category
