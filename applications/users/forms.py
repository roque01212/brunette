from django import forms
from django.contrib.auth import authenticate
#
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'email',
            'full_name',
            'domicilio',
            'ocupation',
            'genero',
            'date_birth',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'type':'email',
                    'placeholder': 'Correo Electronico ...',
                    'class': 'form-control',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'type':'text',
                    'placeholder': 'Nombres ...',
                    'class': 'form-control',
                }
            ),
            'domicilio': forms.TextInput(
                attrs={
                    'required': 'required',
                    'type':'text',
                    'placeholder': 'Domicilio ...',
                    'class': 'form-control',
                }
            ),
            'ocupation': forms.Select(
                attrs={
                    'required': 'required',
                    'placeholder': 'Ocupacion ...',
                    'class': 'form-control',
                }
            ),
            'genero': forms.Select(
                attrs={
                    'required': 'required',
                    'placeholder': 'Genero ...',
                    'class': 'form-control',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'required': 'required',
                    'type': 'date',
                    'class': 'form-control',
                },
            ),
        }
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
    email = forms.CharField(
        label='E-mail',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Correo Electronico',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'contraseña rey'
            }
        )
    )

    def clean(self): 
        self.cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    
    class Meta:

        model = User
        fields = (
            'email',
            'full_name',
            'ocupation',
            'genero',
            'date_birth',
            'is_active',

        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo Electronico ...',
                    'class': 'input-group-field',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres ...',
                    'class': 'input-group-field',
                }
            ),
            'ocupation': forms.Select(
                attrs={
                    'placeholder': 'Ocupacion ...',
                    'class': 'input-group-field',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'input-group-field',
                },
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                },
            ),
        }


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )