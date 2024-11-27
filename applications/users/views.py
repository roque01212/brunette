from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .mixins import AdminPermisoMixin

from django.views.generic import (
    View,
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UserUpdateForm,
)
#
from .models import User
# 


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users_app:User-Lista')

    def form_valid(self, form):
        #
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            full_name=form.cleaned_data['full_name'],
            domicilio=form.cleaned_data['domicilio'],
            ocupation=form.cleaned_data['ocupation'],
            genero=form.cleaned_data['genero'],
            date_birth=form.cleaned_data['date_birth'],
        )
        # enviar el codigo al email del user
        return super(UserRegisterView, self).form_valid(form)


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:Index')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:User-Login'
            )
        )


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/update.html"
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users_app:User-Lista')
    login_url = reverse_lazy('users_app:User-Login')


class UserDeleteView(LoginRequiredMixin,DeleteView):
    model = User
    success_url = reverse_lazy('users_app:User-Lista')
    login_url = reverse_lazy('users_app:User-Login')


class UserListView(AdminPermisoMixin, ListView):
    template_name = "users/lista.html"
    context_object_name = 'usuarios'
    login_url = reverse_lazy('users_app:User-Login')

    def get_queryset(self):
        return User.objects.usuarios_sistema()