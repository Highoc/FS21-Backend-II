from django.contrib import admin

from django.conf import settings
from django.conf.urls import include, url

from core.views import test

from core.views import public, protected
from users.views import upload_photo, upload_file
from topics.views import topic_detail, topic_remove, topic_list

from jsonrpc import jsonrpc_site

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include(('core.urls', 'core'), namespace='core')),
    url(r'^user/', include(('users.urls', 'users'), namespace='users')),
    url(r'^topic/', include(('topics.urls', 'topics'), namespace='topics')),
    url(r'^category/', include(('categories.urls', 'categories'), namespace='categories')),

    url(r'^test/$', test),
    url(r'^api/', jsonrpc_site.dispatch),
    url(r'', include('social_django.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
