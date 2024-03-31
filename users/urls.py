from django.urls import path

from users.views import LoginUser

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
]
