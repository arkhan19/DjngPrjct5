from django.conf.urls import url
from signer.views import *
from django.contrib.auth import *

#this url is for singer application
app_name = 'signer'


urlpatterns = [
    url(r'^signup/', signup, name='signup'),
    url(r'^login/', log_in, name='log_in'),
    url(r'^signout/', signout, name='log_out'),
    # url(r'^reset/', re_set, name='re_set'),


]


