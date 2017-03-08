from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^create$', views.create, name='create'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^delete/(?P<wish_id>\d+)$', views.delete, name='delete'),
    url(r'^add/(?P<wish_id>\d+)$', views.share, name='share'),
    url(r'^cancel/(?P<wish_id>\d+)$', views.cancel, name='cancel'),
    url(r'^wishitem/(?P<wish_id>\d+)$', views.wishitem, name='wishitem'),
    url(r'^additem$', views.additem, name='additem'),
    url(r'^.+$', views.any)

    ]
