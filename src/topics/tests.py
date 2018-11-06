# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import Client

from mock import patch
from users.models import User
from .models import Topic
import topics.views

import factory

import json

class TopicTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user_name', email='testemail@test.test')
        self.user.set_password('test_password')
        self.user.save()

        self.client = Client()
        self.client.login(username='user_name', password='test_password')

    def test_topic_client_login(self):
        topic = Topic.objects.create(name='test_topic', author=self.user)
        response = self.client.get('/topic/{}/detail/'.format(topic.pk))
        self.assertEqual(response.status_code, 200)

    def test_topic_client_logout(self):
        self.client.logout()
        topic = Topic.objects.create(name='test_topic', author=self.user)
        response = self.client.get('/topic/{}/detail/'.format(topic.pk))
        self.assertEqual(response.status_code, 302)

    def test_topic_list_value(self):
        topics = {}
        for i in range(10):
            topics[i] = RandomTopicFactory.create()

        response = self.client.get('/topic/list/')
        content = json.loads(response.content.decode())

        for i in range(10):
            fields = content[i]['fields']
            self.assertEqual(fields['author'], topics[i].author.pk)
            self.assertEqual(fields['name'], topics[i].name)
            self.assertEqual(fields['text'], topics[i].text)


class TopicMockTest(TestCase):

    @patch('topics.views.get_200')
    def test_mock(self, get_200_status_mock):
        get_200_status_mock.return_value = 200
        value = topics.views.get_200()

        self.assertEqual(value, 200)
        self.assertEqual(get_200_status_mock.call_count, 1)


class TopicFixtureTest(TestCase):

    fixtures = ['data.json', 'users.json']

    def setUp(self):
        self.user = User.objects.create(username='user_name', email='testemail@test.test')
        self.user.set_password('test_password')
        self.user.save()

        self.client = Client()
        self.client.login(username='user_name', password='test_password')

    def test_view(self):
        response = self.client.get('/topic/list/')
        content = json.loads(response.content.decode())

        self.assertEqual(content[0]['fields']['name'], 'Topic #1')

class RandomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user_{}'.format(n))
    email = factory.Sequence(lambda  n: 'testemail{}@test.test'.format(n))

class RandomTopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    name  = factory.Sequence(lambda n: 'Topic_#{}'.format(n))
    text  = factory.Sequence(lambda n: 'Text {}'.format(n))
    author = factory.SubFactory(RandomUserFactory)
