from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from Products.models import Variations
from django.conf import settings
from Products.models import Product
# Create your models here.


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", default=1)
    item = models.ForeignKey(Variations)
    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return self.item.title

    def remove(self): # /cart/?item=10&delete=True example of what it will reverse to.
    # return "%s?item=%s&delete=True" %(reverse("cart"), self.item.id, ) # The url we used to get cart item with ? etc
        return self.item.remove_from_cart()


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Variations, through=CartItem) #Through
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.id)
