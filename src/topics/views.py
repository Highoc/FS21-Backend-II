import time

from django.http import JsonResponse

from django import forms
from django.db import models
from django.views.generic import CreateView, UpdateView, DetailView
from django.shortcuts import render, get_object_or_404, reverse, HttpResponse, Http404
from django.core.serializers import serialize
from users.models import User
from topics.models import Topic
from likes.models import Like
from django.forms import ModelForm
from comments.models import Comment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.views.decorators.csrf import csrf_exempt
from jsonrpc import jsonrpc_method
import hashlib, boto3, json

@csrf_exempt
def topic_list(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        j_topics = []
        for topic in topics:
            j_topics.append({
                'id': topic.id,
                'author_id': topic.author_id,
                'name': topic.name,
                'text': topic.text,
                'categories_id': [entry for entry in topic.categories.values_list('id', flat=True)],
            })
        return JsonResponse(j_topics, safe=False)
    else:
        return Http404('Wrong request method')

@csrf_exempt
def topic_add(request):
    if request.method == 'GET':
        return Http404('Wrong request method')
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        data['categories'] = [1]
        form = TopicForm(data=data)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author_id = data['author_id']
            topic.save()
            form.save_m2m()
            publish_topic(topic)
            return JsonResponse({ 'status': 200 })
        else:
            return HttpResponse('Error', status=400)

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'categories', 'text')

import requests, json
from application.settings import CENTRIFUGE_API_KEY

def publish_topic(topic):
    command = {
        "method": "publish",
        "params": {
            "channel": "public:topic",
                "data": {
                    'id': topic.id,
                    'author_id': 1,
                    'name': topic.name,
                    'text': topic.text,
                    'categories_id': [entry for entry in topic.categories.values_list('id', flat=True)],
                }
            }
    }

    api_key = CENTRIFUGE_API_KEY
    data = json.dumps(command)
    print(data)
    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    resp = requests.post("http://centrifugo:9000/api", data=data, headers=headers)
    print(resp.json())

@jsonrpc_method('api.topic_detail')
def topic_detail(request, pk=None):

    topic = get_object_or_404(Topic, id=pk)
    form = CommentForm(request.POST)

    if request.method == "GET":
        Topic.objects.filter(id=pk).update(viewcount=models.F('viewcount') + 1)

    elif request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.topic_id = pk

            comment.save()
            form = CommentForm()



    context = {
        'topic': topic,
        'comment_form': form,
        'comments': topic.topic_comments.all().filter(is_archive=False).filter(comment=None).order_by('created')
    }

    print(context)

    #return HttpResponse(serialize('json', topic), content_type="application/json")
    return render(request, 'topics/detail.html', context)



@jsonrpc_method('api.topic_remove')
def topic_remove(request, pk=None):

    topic = get_object_or_404(Topic, id=pk, author=request.user)

    context = {
        'topic': topic
    }

    #return HttpResponse(serialize('json', context['topic']), content_type="application/json")
    return render(request, 'topics/remove.html', context)


class TopicsListForm(forms.Form):

    sort = forms.ChoiceField(
        choices=(
            ('name', 'Name asc'),
            ('-name', 'Name desc'),
            ('id', 'By Id'),
            ('created', 'By date'),
        ),
        required=False)
    category = forms.CharField(required=False)
    search = forms.CharField(required=False)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Добавить комментарий'))

class TopicEdit(UpdateView):
    form_class = TopicForm
    model = Topic
    template_name = 'topics/edit.html'
    context_object_name = 'topic'

    def get_queryset(self):
        queryset = super(TopicEdit, self).get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('topics:detail', kwargs={'pk': self.object.pk})


def topic_comments(request, pk=None):

    topic = get_object_or_404(Topic, id=pk)
    context = {
        'comments': topic.topic_comments.all().filter(is_archive=False).filter(comment=None).order_by('created')
    }

    return render(request, 'topics/widgets/comment_all.html', context)

def likes_counter(request, pk=None):

    topic = get_object_or_404(Topic, id=pk)
    context = {
        'count': topic.topic_likes.all().filter(is_archive=False).count()
    }

    return render(request, 'topics/widgets/like_counter.html', context)

def likes_update(request, pk=None):

    topic = get_object_or_404(Topic, id=pk)

    like = None
    if topic.topic_likes.filter(topic=topic, author=request.user).count() == 1:
        like = topic.topic_likes.get(topic=topic, author=request.user)

    if like == None:
        like = Like()
        like.author = request.user
        like.topic = topic
        like.save()
        return HttpResponse("Дизлайк")

    else:
        if like.is_archive:
            like.is_archive = False
            like.save()
            return HttpResponse("Лайк")

        else:
            like.is_archive = True
            like.save()
            return HttpResponse("Дизлайк")


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Ответить'))


def topic_comment_add(request, pk=None, parent_id=None):

    topic = get_object_or_404(Topic, id=pk)
    parent_comment = get_object_or_404(Comment, id=parent_id)
    form = AddCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.topic = topic
        comment.comment = parent_comment
        comment.save()
        return HttpResponse("OK")

    context = {
        'comment_form': form,
        'topic': topic,
        'parent_comment': parent_comment
    }

    return render(request, 'topics/widgets/comment_add.html', context)

def get_200():
    time.sleep(10)
    return 200;