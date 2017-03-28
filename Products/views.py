from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Create your views here.
from django.db.models import Q #Q lookups
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Product, Variations
from .forms import VariationInventoryFormSet

from .mixins import StaffRequiredMixin


class ProductDetailView(DetailView):
    model = Product  # name of the class model
    template_name = "products/product_detail.html"


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")
        return context
        # This function will help us search items, it's using Q lookups, and query are being passed to db through it

    def get_queryset(self, *args, **kwargs):
        q = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            q = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            #to use both text and integer for query set we will need to add extra logic
            try:
                q2 = self.model.objects.filter(
                    Q(price=query)
                )
                q = (q | q2).distinct() #makes sure that we are not getting two objects. distinct will give only 1.
            except:
                pass
        return q


class VariationsListView(StaffRequiredMixin, ListView):
    model = Variations
    queryset = Variations.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(VariationsListView, self).get_context_data(*args, **kwargs)
        context["formset"] = VariationInventoryFormSet()
        return context

    def get_queryset(self, *args, **kwargs):
        # q = super(VariationsListView, self).get_queryset(*args, **kwargs)
        # query = self.request.GET.get("q")
        product_pk = self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            q = Variations.objects.filter(product=product)
        return q

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                if new_item.title:
                    product_pk = self.kwargs.get("pk")
                    product = get_object_or_404(Product, pk=product_pk)
                    new_item.product = product
                    new_item.save()
            messages.success(request, "Your inventory and pricing has been updated.")
            return redirect("products_list.html")
        raise Http404
# def product_detail_view_function(request, id):
#     product_instance = Product.objects.get(id=id)
#     template = "products/product_detail.html"
#     context = {
#         "object": product_instance
#     }
#     return render(request, template, context)

# Using CBV not Function based views.
