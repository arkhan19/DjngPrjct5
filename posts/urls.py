from django.conf.urls import url
from posts.views import *
#this url is for singer application
app_name = 'posts'

urlpatterns = [
    url(r'^create/', create, name='create'),
    url(r'^user/(?P<fk>\w+)/', auser, name='postings'),
    #   url(r'^login/', log_in, name='log_in'),
    # regex PostID/commendup [0-9] any numnber + = any length
    url(r'^(?P<pk>[0-9]+)/up', c_up, name='counter_up'),
    # regex PostID/commenddown
    url(r'^(?P<pk>[0-9]+)/down', c_down, name='counter_down'),
]
