import time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from . import models
from .forms import LoginForm, RegisterForm, EditForm, PasswordForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from .jwthelper import jwt_encode, jwt_decode
from .mailhelper import sendmail


def index(request):
    return render(request, 'dating/index.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect('/')

    if request.method == "POST":
        form = LoginForm(request.POST)
        message = "Some fields are invalid"
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = models.User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.email
                    return redirect('/')
                else:
                    message = "Password is wrong"
            except:
                message = "User not found"
        return render(request, 'dating/login.html', locals())

    form = LoginForm()
    return render(request, 'dating/login.html', locals())

def send_verify_email(user):

    link = "http://127.0.0.1:8000/verify_email?token=%s" % (
        jwt_encode({
            "user_id": user.id,
            "exp": int(time.time() + 60*60*24*60)
        })
    )
    text = "Verify your email by opening %s" % link
    html = """\
    <html>
    <head></head>
    <body>
        Verify your email by opening <a href="%s">this link</a>
    </body>
    </html>
    """ % link
    sendmail(user.email, "Verify email", text, html)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        message = "Some fields are invalid"
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            gender = form.cleaned_data['gender']
            if password != confirm_password:
                message = "Confirm password not match"
                return render(request, 'dating/register.html', locals())
            else:
                user = models.User.objects.filter(email=email)
                if user:
                    message = 'Email is already registered'
                    return render(request, 'dating/register.html', locals())

                user = models.User.objects.create()
                user.name = name
                user.password = make_password(password)
                user.email = email
                user.gender = gender
                user.save()
                send_verify_email(user)

                return redirect('/login/')
        return render(request, 'dating/register.html', locals())
    form = RegisterForm()
    return render(request, 'dating/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    request.session.flush()
    return redirect('/')


def verify_email(request):
    try:
        info = jwt_decode(request.GET.get('token'))
        user = models.User.objects.get(pk=info['user_id'])
        user.email_verified = True
        user.save()
        success = True
    except:
        success = False
    return render(request, 'dating/verify_email.html', locals())


def edit(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    
    user = models.User.objects.get(pk=request.session['user_id'])
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=user)
        message = "Some fields are invalid"
        if form.is_valid():
            form.save()
            message = "Save successfully!"
    form = EditForm(instance=user)
    return render(request, 'dating/edit.html', locals())


def password(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    
    if request.method == "POST":
        form = PasswordForm(request.POST)
        message = "Some fields are invalid"
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                message = "Confirm password not match"
                return render(request, 'dating/password.html', locals())
            else:
                user = models.User.objects.get(pk=request.session['user_id'])
                
                user.password = make_password(password)
                user.save()
                message = "Change password successfully!"
        return render(request, 'dating/password.html', locals())
    form = PasswordForm()
    return render(request, 'dating/password.html', locals())


class DiscoverView(ListView):
    paginate_by = 6
    model = models.User
    template_name = 'dating/discover.html'
    context_object_name = 'users'

    def get_queryset(self):
        user_id = self.request.session['user_id']
        return models.User.objects.filter(~Q(id=user_id)).order_by('-last_active')

    def render_to_response(self, context):
        if not self.request.session.get('is_login', None):
            return redirect("/")
        return super(DiscoverView, self).render_to_response(context)

class UserView(DetailView):
    model = models.User
    template_name = 'dating/user.html'
    context_object_name = 'user'

    def render_to_response(self, context):
        if not self.request.session.get('is_login', None):
            return redirect("/")
        return super(UserView, self).render_to_response(context)

    def get_object(self, **kwargs):
        print(kwargs)
        return models.User.objects.get(id=self.kwargs['id'])


class ChatView(ListView):
    paginate_by = 5
    template_name = 'dating/chats.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        user_id = self.request.session['user_id']
        return models.Room.objects\
            .filter(Q(user1=user_id) | Q(user2=user_id))\
            .order_by('-updated_at')\
            .prefetch_related('user1', 'user2')

    def render_to_response(self, context):
        if not self.request.session.get('is_login', None):
            return redirect("/")
        return super(ChatView, self).render_to_response(context)


def chat(request, id):
    if not request.session.get('is_login', None):
        return redirect("/")
    me = models.User.objects.get(pk=request.session['user_id'])
    user = models.User.objects.get(pk=id)
    if me.id == user.id:
        return redirect("/discover")

    jwt_token = jwt_encode({
        "user_id": me.id,
        "exp": int(time.time() + 60*60*24*60)
        })

    try:
        room = models.Room.objects\
            .get(Q(user1=me, user2=user) | Q(user2=me, user1=user))
    except models.Room.DoesNotExist:
        room = models.Room.objects.create(user1=me, user2=user)
    
    messages = room.message_set.all().prefetch_related('user')

    return render(request, 'dating/chat.html', locals())
