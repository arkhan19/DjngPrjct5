from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponseRedirect

# Create your views here.
from Products.models import Variations
from cart.models import Cart, CartItem

from django.views.generic.detail import SingleObjectMixin #Will help in getting objects on current HTTP request


class CartView(SingleObjectMixin, View):
    model = Cart

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        # If use is not logged in
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)

        # if user is logged in
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        # #If use is not logged in
        # cart_id = request.session.get("cart_id")
        # if cart_id == None:
        #     cart = Cart()
        #     cart.save()
        #     cart_id = cart.id
        #     request.session["cart_id"] = cart_id
        # cart = Cart.objects.get(id=cart_id)
        #
        # #if user is logged in
        # if request.user.is_authenticated():
        #     cart.user = request.user
        #     cart.save()
        cart = self.get_object() #Working with get_object defined above.
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete")
        if item_id:
            item_instance = get_object_or_404(Variations, id=item_id)
            qty = request.GET.get("qty")
            cart = Cart.objects.all().first()
            cart_item = CartItem.objects.get_or_create(cart=cart, item=item_instance)[0]
            if delete_item:
                cart_item.quantity = qty
            else:
                cart_item.quantity = qty
                cart_item.save()
        return HttpResponseRedirect("/")

