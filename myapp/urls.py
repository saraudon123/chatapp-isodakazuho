from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login_view'),
    path('friends', views.FriendView.as_view(), name='friends'),
    path('talk_room/<int:pk>/', views.TalkRoomView.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),
]
