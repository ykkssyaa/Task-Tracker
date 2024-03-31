from django.urls import path

import users.views as views

urlpatterns = [
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('', views.UserList.as_view(), name='user_list'),
    path('<str:username>', views.UserPage.as_view(), name='user_page'),
]
