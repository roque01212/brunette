from django.urls import path

from . import views

app_name = "users_app"

urlpatterns = [
    path(
        '', 
        views.LoginUser.as_view(),
        name='User-Login',
    ),
    path(
        'users/register/', 
        views.UserRegisterView.as_view(),
        name='User-Register',
    ),
    path(
        'users/logout/', 
        views.LogoutView.as_view(),
        name='User-Logout',
    ),
    path(
        'users/update-password/<pk>/', 
        views.UpdatePasswordView.as_view(),
        name='User-Update_Password',
    ),
    path(
        'users/update/<pk>/', 
        views.UserUpdateView.as_view(),
        name='User-Update',
    ),
    path(
        'users/delete/<pk>/', 
        views.UserDeleteView.as_view(),
        name='user-delete',
    ),
    path(
        'users/lista/', 
        views.UserListView.as_view(),
        name='User-Lista',
    ),
]