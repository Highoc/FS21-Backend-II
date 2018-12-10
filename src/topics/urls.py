from django.conf.urls import url
from topics.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(
        r'^list/$',
        topic_list,
        name='list'
    ),

    url(
        r'^add/$',
        topic_add,
        name='add'
    ),

    url(
        r'^(?P<pk>\d+)/edit/$',
        login_required(TopicEdit.as_view()),
        name='edit'
    ),

    url(
        r'^(?P<pk>\d+)/detail/$',
        login_required(topic_detail),
        name='detail'
    ),

    url(
        r'^(?P<pk>\d+)/remove/$',
        login_required(topic_remove),
        name='remove'
    ),

    url(
        r'^(?P<pk>\d+)/detail/comments/$',
        login_required(topic_comments),
        name='comments'
    ),

    url(
        r'^(?P<pk>\d+)/addcomment/(?P<parent_id>\d+)/$',
        login_required(topic_comment_add),
        name='comment_add'
    ),

    url(
        r'^(?P<pk>\d+)/detail/likes/$',
        login_required(likes_counter),
        name='likes'
    ),

    url(
        r'^(?P<pk>\d+)/addlike/$',
        login_required(likes_update),
        name='like_add'
    )
]