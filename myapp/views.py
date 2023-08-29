from ast import keyword
from atexit import register
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from .models import CustomUser, Talk
from django.urls import reverse_lazy, reverse
from .forms import SignUpForm, LoginForm, TalkRoomForm, UsernameChangeForm, FriendSearchForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.db.models import Max, Q
from django.db.models.functions import Greatest, Coalesce
from django.views.generic.edit import CreateView, UpdateView


def index(request):
    return render(request, "myapp/index.html")

# def signup_view(request):
#     if request.method == 'GET':
#         form = SignUpForm()
#     elif request.method == 'POST':
#         form = SignUpForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data["username"]
#             email = form.cleaned_data["email"]
#             password = form.cleaned_data["password1"]
#             img = form.cleaned_data["img"]
#             user = authenticate(username=username, email=email, password=password, img=img)
#             login(request, user)

#             return redirect('index')
        
#     context = {"form":form}
#     return render(request, "myapp/signup.html", context)

class SignupView(CreateView):
    template_name = 'myapp/signup.html'
    model = CustomUser
    form_class = SignUpForm
    success_url = '/'
    # success_url = reverse_lazy('myapp:index')



# def login_view(request):
#     if request.method == 'GET':
#         form = LoginForm()
#     elif request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():

#     return render(request, "myapp/login.html")

class LoginView(LoginView):
    template_name = "myapp/login.html"
    form_class = LoginForm


class FriendView(LoginRequiredMixin, ListView):
    template_name = "myapp/friends.html"
    context_object_name = 'friends'
    model = CustomUser

    # def get_queryset(self):
    #     queryset = CustomUser.objects.exclude(id=self.request.user.id).annotate(
    #         receivetime = Max("senddesu__time", filter=Q(senddesu__receiver=self.request.user)),
    #         sendtime = Max("receivedesu__time", filter=Q(receivedesu__sender=self.request.user)),
    #         talktime = Greatest("sendtime", "receivetime",),
    #         latesttime = Coalesce("talktime", "receivetime", "date_joined",),
    #     ).order_by("-latesttime").all()

    #     form = FriendSearchForm()
    #     if form.is_valid():
    #         keyword = form.cleaned_data['keyword']
    #         queryset = queryset.filter(username__contains=keyword)

    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FriendSearchForm(self.request.GET)

        if form.is_valid():
            print("a")
            keyword = form.cleaned_data.get("keyword")
            friends = CustomUser.objects.exclude(id=self.request.user.id).annotate(
                receivetime = Max("senddesu__time", filter=Q(senddesu__receiver=self.request.user)),
                sendtime = Max("receivedesu__time", filter=Q(receivedesu__sender=self.request.user)),
                talktime = Greatest("sendtime", "receivetime",),
                latesttime = Coalesce("talktime", "receivetime", "date_joined",),
            ).order_by("-latesttime").filter(username__contains=keyword)
        else:
            print("A")
            friends = CustomUser.objects.exclude(id=self.request.user.id).annotate(
                receivetime = Max("senddesu__time", filter=Q(senddesu__receiver=self.request.user)),
                sendtime = Max("receivedesu__time", filter=Q(receivedesu__sender=self.request.user)),
                talktime = Greatest("sendtime", "receivetime",),
                latesttime = Coalesce("talktime", "receivetime", "date_joined",),
            ).order_by("-latesttime").all()

        context["friends"] = friends
        context["form"] = form
        return context


class TalkRoomView(LoginRequiredMixin, CreateView):
    template_name = "myapp/talk_room.html"
    form_class = TalkRoomForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        friend_id = self.kwargs['pk']
        friend = CustomUser.objects.get(id=friend_id)
        talks = Talk.objects.filter(
            Q(sender=self.request.user, receiver=friend) |
            Q(receiver=self.request.user, sender=friend)
        ).order_by("time")
        context["friend"] = friend
        context["talks"] = talks
        return context

    def form_valid(self, form):
        friend_id = self.kwargs['pk']
        friend = CustomUser.objects.get(id=friend_id)
        talkform = form.save(commit=False)
        talkform.sender = self.request.user
        talkform.receiver = friend
        talkform.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('talk_room', kwargs={'pk': self.kwargs['pk']})


def setting(request):
    return render(request, "myapp/setting.html")

# class UsernameChangeView(LoginRequiredMixin, CreateView):
#     template_name = "myapp/username_change.html"
#     form_class = UsernameChangeForm

#     def form_valid(self, form):
#         form = form.save(commit=False)
#         form.user = self.request.user
#         form.save()
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('username_change_done')
    
class UsernameChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ('username',)
    template_name = "myapp/username_change.html"
    success_url = reverse_lazy('username_change_done')

    def get_object(self):
        me = self.request.user
        return me

class EmailChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ('email',)
    template_name = "myapp/email_change.html"
    success_url = reverse_lazy('email_change_done')

    def get_object(self):
        me = self.request.user
        return me

def username_change_done(request):
    return render(request, "myapp/username_change_done.html")

def email_change_done(request):
    return render(request, "myapp/email_change_done.html")

class IconChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ('img',)
    template_name = "myapp/icon_change.html"
    success_url = reverse_lazy('icon_change_done')

    def get_object(self):
        me = self.request.user
        return me

def icon_change_done(request):
    return render(request, "myapp/icon_change_done.html")

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "myapp/password_change.html"

class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "myapp/password_change_done.html"

class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = "myapp/setting.html"