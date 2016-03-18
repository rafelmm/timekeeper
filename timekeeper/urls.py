# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'timekeeper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('timekeeper.apps.smtk.urls', namespace="smtk")),
    url(r'^admin/', include(admin.site.urls)),
    
]
