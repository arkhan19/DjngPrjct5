from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework import serializers, viewsets, permissions
from rest_framework_jwt.authentication import *
from .models import Posts


class PostSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        # Pointing to the model to be serialized
        model = Posts
        # Pointing to fields which will be serialized
        fields = [
            'id',
            'title',
            'pub_date',
            'commends',
            'url',
        ]

class PostViewSet(viewsets.ModelViewSet):
    # Authentication to view or get the data ability. DOESN'T specify permissions.
    authentication_classes = [SessionAuthentication,BaseAuthentication, JSONWebTokenAuthentication]
    # Permissions specifications
    permission_classes = [permissions.IsAuthenticated, ] # Will need to be login to view data now.
    queryset = Posts.objects.all()
    serializer_class = PostSerializers

