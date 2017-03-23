"""vs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from views import ProductListView
from views import ProductDetailView
#app_name = 'Products' #What does this do? It was causing url malfunctions, please find out when finished.
# FBV Import
# from vs.products.views import product_detail_view_function



urlpatterns = [
    # url(r'^(?P<id>\d+)', product_detail_view_function, name='product_detail_view_function'), # URL Pattern for FBV
    url(r'^$', ProductListView.as_view(), name='products'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='productsd'), #cbv and as_view() to get a CB view
]
