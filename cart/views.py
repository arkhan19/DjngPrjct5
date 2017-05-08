from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic.detail import SingleObjectMixin #Will help in getting objects on current HTTP request
from django.core.urlresolvers import reverse
# Create your views here.
from Products.models import Variations
from cart.models import Cart, CartItem


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "cart/views.html"

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
        delete_item = request.GET.get("delete", False)
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Variations, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
             # if it's not added it's False and still going through JSON response
            if created:
                item_added = True
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
            # if not request.is_ajax():
            #     # return if saved and set, it should be sent back and not changed if page is refreshed
            #     return HttpResponseRedirect(reverse("cart"))
            #     #return cart_item.cart.get_absolute_url()

        # handling AJAX call
        if request.is_ajax():
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None
            try:
                total_items = cart_item.cart.items.count()
            except:
                total_items = 0
            data = {
                "deleted": delete_item,
                "item_added":item_added,
                "line_total": total,
                "sub_total": subtotal,
                "total_items": total_items
            }

            # print (request.GET.get("item"))
            return JsonResponse(data)

        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)


class ItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id == None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()

            request.session["item_count"] = count
            return JsonResponse({"count":count})
        else:
            raise Http404
