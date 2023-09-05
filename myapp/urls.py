from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),

    # path('signup', views.SignupView.as_view(), name='signup'),

    # path('login', views.LoginView.as_view(), name='login_view'),

    path('friends', views.FriendView.as_view(), name='friends'),
    path('talk_room/<int:pk>/', views.TalkRoomView.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change', views.UsernameChangeView.as_view(), name='username_change'),
    path('username_change_done', views.username_change_done, name='username_change_done'),
    path('email_change', views.EmailChangeView.as_view(), name='email_change'),
    path('email_change_done', views.email_change_done, name ='email_change_done'),
    path('img_change', views.IconChangeView.as_view(), name='icon_change'),
    path('icon_change_done', views.icon_change_done, name='icon_change_done'),
    path('password_change', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]
