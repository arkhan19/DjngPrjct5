from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Product



# def product_detail_view_function(request, id):
#     product_instance = Product.objects.get(id=id)
#     template = "products/product_detail.html"
#     context = {
#         "object": product_instance
#     }
#     return render(request, template, context)

# Using CBV not Function based views.


class ProductDetailView(DetailView):
    model = Product  # name of the class model
    template_name = "products/product_detail.html"

class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["now"] = timezone.now()
        return context
