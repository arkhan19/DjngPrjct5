from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
# Create your models here.


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):  # this will override the .all query set
        return self.get_queryset().active()

    def get_related(self, instance):
        products_one = self.get_queryset().filter(categories__in = instance.categories.all())
        products_two = self.get_queryset().filter(default=instance.default)
        qs = (products_one | products_two).exclude(id=instance.id).distinct()
        return qs


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)

    categories = models.ManyToManyField('Category', blank=True)  # Many Product can have Many Categories # if you use without quotes
    default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)          # Default Category # Error will come, this makes to lk in the file.


    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #return "/products/%s"%(self.pk)
        return reverse("productsd", kwargs={"pk": self.pk})

    def get_iamge_url(self):
        img = self.productimage_set.first() # get's first item on query set or none
        if img:
            return img.image.url
        return img # noneeeeee


class Variations(models.Model):
    product = models.ForeignKey(Product) # associating this variation to a product itself, WTH of Foreign key.
    title = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(default='-1', null=True, blank=True)    #-1 = unlimited

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()


def product_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variations_set.all() # QS manager wala == variations = Variation.object.filter(product=product)
    # with this we are not calling up Variation directly, just using the instance to explore it and play with it. Nice:)
    if variations.count()== 0:
        new_var = Variations() # here we are calling the class, and passing it to new_var Important, small V and cap V
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()

post_save.connect(product_saved_receiver, sender=Product) #Product is the sender, Post_save.connect is connected the
# receiver and sender
# after this we will have a default value, this means is that we are able to provide a product with default value
# if it doesn't have any variations.


# Product Images
class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='')

    def __unicode__(self):
        return self.product.title
# Product Category


class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

def image_upload_to_featured(instance, filename):
    title= instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
    return "products/%s/featured/%s" %(slug, new_filename)

class ProductFeatured(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to_featured)
    title = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=220, null=True, blank=True)
    text_right = models.BooleanField(default=False)
    show_price = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product.title