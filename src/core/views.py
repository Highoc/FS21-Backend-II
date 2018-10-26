from django.http.response import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect, HttpResponse

from application import settings

from django.shortcuts import render
from django.urls import reverse_lazy

from users.models import User
from core.models import File

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as OldUserCreationForm
from django.contrib.auth import login, logout, authenticate

from django.views import generic

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit

from jsonrpc import jsonrpc_method
import base64, hashlib, json


def core_index(request):
    return render(request, 'core/index.html')


@jsonrpc_method( 'api.get_file' )
def get_file(request, filename):
    key = generate_key(filename)
    file = File.objects.filter(key=key, owners=request.user).first()
    print(filename)

    if file is None:
        return HttpResponseNotFound('404')

    else:
        responce = HttpResponse()
        responce['X-Accel-Redirect'] = '/protected/{}/{}/'.format(settings.AWS_STORAGE_BUCKET_NAME, key)
        return responce


def generate_key(filename):
    h = hashlib.new('md5')
    h.update(filename.encode('utf-8'))
    return h.hexdigest()


class UserCreationForm(OldUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('password1'),
            Field('password2'),
            Field('email'),
            ButtonHolder(
                Submit('register', 'Signup', css_class='btn-primary')
            )
        )

class LoginForm(AuthenticationForm):

    template_name = "core/login.html"

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('password'),
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )


class SignupView(generic.CreateView):

    form_class = RegistrationForm
    model = User
    template_name = 'core/register.html'
    success_url = reverse_lazy('core:login')

    def form_valid(self, form):
        form.save()
        return super(SignupView, self).form_valid(form)

class LoginView(generic.FormView):
        form_class = LoginForm
        success_url = reverse_lazy('users:index')
        template_name = 'core/login.html'

        def form_valid(self, form):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(self.request, user)
                return super(LoginView, self).form_valid(form)
            else:
                return self.form_invalid(form)

class LogoutView(generic.RedirectView):
    url = reverse_lazy('core:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
