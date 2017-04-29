from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from Products.models import Variations
from django.conf import settings
from Products.models import Product
from django.db.models.signals import pre_save
from decimal import Decimal
# Create your models here.


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", default=1)
    item = models.ForeignKey(Variations)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2, default=19)

    def __unicode__(self):
        return self.item.title

    def remove(self): # /cart/?item=10&delete=True example of what it will reverse to.
    # return "%s?item=%s&delete=True" %(reverse("cart"), self.item.id, ) # The url we used to get cart item with ? etc
        return self.item.remove_from_cart()

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity

    if qty >=1:
        price = instance.item.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Variations, through=CartItem) #Through
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.id)
