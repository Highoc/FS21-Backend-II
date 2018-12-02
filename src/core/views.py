from django.http.response import HttpResponseNotFound, HttpResponseRedirect, JsonResponse, Http404, HttpResponse

from application import settings

from django.middleware.csrf import get_token

from users.models import User
from core.models import File

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as loginUser, logout as logoutUser

from django.views.decorators.csrf import csrf_exempt

from jsonrpc import jsonrpc_method
import hashlib, boto3, json


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return Http404('Wrong request method')
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = AuthenticationForm(data=data)
        if form.is_valid():
            user = form.get_user()
            loginUser(request, user)
            return JsonResponse({
                'userId': user.pk,
                'token': generate_key(user.get_username())
            })
        else:
            return HttpResponse('Unauthorized', status=401)


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

@csrf_exempt
def register(request):
    if request.method == 'GET':
        return Http404('Wrong request method')
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = RegistrationForm(data=data)
        if form.is_valid():
            form.save()
            return JsonResponse({ 'status': 200 })
        else:
            return HttpResponse('Registration error', status=401)

@csrf_exempt
def logout(request):
    logoutUser(request)
    return JsonResponse({ 'status': 200 })

def test(request):
    if request.method == 'GET':
        return JsonResponse({ 'csrfmiddlewaretoken': get_token(request)})
    elif request.method == 'POST':
        return JsonResponse({ 'status': 'OK'})

@jsonrpc_method( 'api.public' )
def public(request, filename):
    key = generate_key(filename)
    file = File.objects.filter(key=key, owners=request.user).first()

    if file is None:
        return HttpResponseNotFound('404')

    else:
        return HttpResponseRedirect('/protected/{}/{}/'.format(settings.AWS_STORAGE_BUCKET_NAME, key))


@jsonrpc_method( 'api.protected' )
def protected(request, bucket, key):

    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket,
            'Key': 'files/{}/{}'.format(request.user.pk, key),
        }
    )

    return JsonResponse({ 'url': url })


def generate_key(filename):
    h = hashlib.new('md5')
    h.update(filename.encode('utf-8'))
    return h.hexdigest()
