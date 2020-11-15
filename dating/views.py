from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from . import models
from .forms import LoginForm, RegisterForm, EditForm, PasswordForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView


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
                return redirect('/login/')
        return render(request, 'dating/register.html', locals())
    form = RegisterForm()
    return render(request, 'dating/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    request.session.flush()
    return redirect('/')


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
    ordering = ['-last_active']

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
