from django.conf.urls import patterns, url

from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

from plag import views, const

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^index-trial/$', views.IndexTrialView.as_view(), name='index_trial'),


                       url(r'^about-us/$', TemplateView.as_view(template_name='plag/static/about.html'), name='about'),

                       url(r'^contact-us/$', TemplateView.as_view(template_name='plag/static/contact_us.html'),
                           name='contact')
                       )
