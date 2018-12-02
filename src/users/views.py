from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
import base64, hashlib, json
from django.views.decorators.csrf import csrf_exempt
from jsonrpc import jsonrpc_method
from users.models import User
from core.models import File
from django.http.response import HttpResponseNotFound, JsonResponse, Http404, HttpResponse
from django.core.serializers import serialize
def user_index(request):
    return render(request, 'users/index.html')

def user_info(request):
    return render(request, 'users/info.html')



@jsonrpc_method( 'api.upload_photo' )
def upload_photo( request, user_pk, content_base64 ):
    file_content = base64.b64decode( content_base64 ).decode('utf-8')

    user = User.objects.filter(id=user_pk).first()
    key = generate_key(user.username)

    user.photo.save( '{}/{}'.format(user.id, key), ContentFile(file_content.encode('utf-8')))

    return key


@jsonrpc_method( 'api.upload_file' )
def upload_file( request, user_pk, file_json ):
    file = json.loads(file_json)

    content = base64.b64decode( file['content'] ).decode('utf-8')
    key = generate_key( file['filename'] )
    owner = User.objects.filter( id=user_pk ).first()

    new_file = File.objects.filter(key=key, owners=owner).first()
    if not new_file is None:
        new_file.content.save('{}/{}'.format(user_pk, key), ContentFile(content.encode('utf-8')))
        new_file.save()
    else:
        new_file = File()
        new_file.key = key
        new_file.name = file['filename']
        new_file.mime = file['mime_type']
        new_file.content.save('{}/{}'.format(user_pk, key), ContentFile(content.encode('utf-8')))
        new_file.save()
        new_file.owners.add(owner)

    return key


def generate_key(filename):
    h = hashlib.new('md5')
    h.update(filename.encode('utf-8'))
    return h.hexdigest()

@csrf_exempt
def get_user(request, id=None):
    if request.method == 'GET':
        user = User.objects.get(id=id)
        if not user is None:
            return JsonResponse({
                'id': user.id,
                'login': user.username,
                'name': user.first_name,
                'surname': user.last_name,
            })
        else:
            return HttpResponseNotFound()
    elif request.method == 'POST':
        return Http404('Wrong request method')

@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        j_users = []
        for user in users:
            j_users.append({
                'id': user.id,
                'login': user.username,
                'name': user.first_name,
                'surname': user.last_name,
            })
        return JsonResponse(j_users, safe=False)
    elif request.method == 'POST':
        return Http404('Wrong request method')