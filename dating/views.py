from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    template = 'index.html'
    context = {}
    return render(request, template, context)

def login(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        message = "Some fields are empty"
        if email and password:
            email = email.strip()
            try:
                user = models.User.objects.get(email=email)
                if user.password == password:
                    return redirect('/index/')
                else:
                    message = "Password is wrong"
            except:
                message = "User not found"

        return render(request, 'dating/login.html', {"message": message})

    return render(request,'dating/login.html')

def register(request):
    pass
    return render(request,'dating/register.html')

def logout(request):
    pass
    return redirect('/index/')