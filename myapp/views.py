from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from.forms import SignUpForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            img = form.cleaned_data["img"]
            user = authenticate(username=username, email=email, password=password, img=img)
            login(request, user)

            return redirect('index')
        
    context = {"form":form}
    return render(request, "myapp/signup.html", context)

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
