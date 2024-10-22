from django.urls import path

from . import views

app_name = "users_app"

urlpatterns = [
    path(
        '', 
        views.LoginUser.as_view(),
        name='user-login',
    ),
    path(
        'users/logout/', 
        views.LogoutView.as_view(),
        name='User-Logout',
    ),
    path(
        'users/lista/', 
        views.UserListView.as_view(),
        name='User-Lista',
    ),
]