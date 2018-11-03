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

]