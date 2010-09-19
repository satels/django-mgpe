#encoding:utf8
from django.conf.urls.defaults import *

urlpatterns = patterns('django_mgpe.xml.server',
    url(r'^$',  'mgpe' , name='mgpe_main'),
)
