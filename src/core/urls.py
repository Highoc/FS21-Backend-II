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
        r'^get_file/(?P<key>\w+)/$',
        get_file,
        name='get_file'
    )
]