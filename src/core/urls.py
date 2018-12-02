from django.conf.urls import url
from core.views import *

urlpatterns = [

    url(
        r'^login/$',
        login,
        name='login'
    ),

    url(
        r'^logout/$',
        logout,
        name='logout'
    ),

    url(
        r'^register/$',
        register,
        name='register'
    ),

    url(
        r'^public/(?P<filename>\w+.\w+)/$',
        public,
        name='public'
    ),
    url(
        r'^protected/(?P<bucket>\w+)/(?P<key>\w+)/$',
        protected,
        name='protected'
    ),
]