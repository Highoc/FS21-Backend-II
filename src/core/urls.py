from django.conf.urls import url
from core.views import *

urlpatterns = [
    url(
        r'^$',
        core_index,
        name='index'
    ),

    url(
        r'^login/$',
        LoginView.as_view(),
        name='login'
    ),

    url(
        r'^logout/$',
        LogoutView.as_view(),
        name='logout'
    ),

    url(
        r'^register/$',
        SignupView.as_view(),
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