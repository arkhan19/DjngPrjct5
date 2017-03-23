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
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
from posts import views
from posts.serializers import PostViewSet
from rest_framework_jwt.views import obtain_jwt_token

# Creating a Router to direct to api of posts.
router = routers.DefaultRouter()

# Registering the router to view the post's meta data
router.register(r"Posts", PostViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^accounts/', include('signer.urls')),
    url(r'^posts/', include('posts.urls')),
    url(r'^products/', include('Products.urls')),
    url(r'^reset/', include('password_reset.urls')),

    url(r'^api/token/auth/$', obtain_jwt_token), #JWT auth url
    url(r'^postapi/auth/', include('rest_framework.urls', namespace='rest_framework')), # adds login on drf page
    url(r'^postapi/', include(router.urls)),
]
