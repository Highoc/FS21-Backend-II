from django.conf.urls import url
from users.views import *

urlpatterns = [
    url(
        r'^home/$',
        user_index,
        name='index'
    ),

    url(
        r'^info/$',
        user_info,
        name='info'
    ),

    url(
        r'^get_user/(?P<id>\d+)/$',
        get_user,
        name='get_user'
    ),

    url(
        r'^get_all_users/$',
        get_all_users,
        name='get_all_users'
    ),
]