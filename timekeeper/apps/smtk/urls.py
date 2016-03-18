# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import indexView, storyView, taskView, calendarView

urlpatterns = patterns('',
    url(r'^$', indexView, name='index'),
    url(r'^story/(?P<storyid>\d+)/$', storyView, name="story"),
    url(r'^task/(?P<taskid>\d+)/$', taskView, name="task"),
    url(r'^calendar/$', calendarView, name="calendar"),
)