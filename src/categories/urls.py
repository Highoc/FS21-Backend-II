from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from categories.views import *

urlpatterns = [
    url(
        r'^add/$',
        login_required(category_add),
        name='add'
    ),

    url(
      r'^(?P<pk>\d+)/edit/$',
        login_required(category_edit),
        name='edit'
    ),

    url(
        r'^list/$',
        login_required(category_list),
        name='list'
    ),

    url(
        r'^(?P<pk>\d+)/remove/$',
        login_required(category_remove),
        name='remove'
    ),

    url(
        r'^(?P<pk>\d+)/detail/$',
        login_required(category_detail),
        name='detail'
    ),
]