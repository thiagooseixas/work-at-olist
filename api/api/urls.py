from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest import views
from rest.models import Call
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'calls', views.CallViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^call/$', views.save_call),
    url(r'^get-telephone-bill/$', views.get_telephone_bill),
    url(r'^call-record/$', views.call_record)
]

#urlpatterns = format_suffix_patterns(urlpatterns)
