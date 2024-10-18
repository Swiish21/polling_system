from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4