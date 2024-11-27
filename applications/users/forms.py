from django import forms
from django.contrib.auth import authenticate
from datetime import date
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
        label='Repetir Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = User
        fields = ('email', 'full_name', 'domicilio', 'ocupation', 'genero', 'date_birth')
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Correo Electrónico',
                'class': 'form-control',
            }),
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Nombre Completo',
                'class': 'form-control',
            }),
            'domicilio': forms.TextInput(attrs={
                'placeholder': 'Domicilio',
                'class': 'form-control',
                'autocomplete': 'new-password',
                'name': 'user_address',
                'type': 'text',
            }),
            'ocupation': forms.Select(attrs={
                'class': 'form-select',
            }),
            'genero': forms.Select(attrs={
                'class': 'form-select',
            }),
            'date_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_date_birth(self):
        date_birth = self.cleaned_data.get("date_birth")
        if date_birth:
            today = date.today()
            age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))
            if age < 18:
                raise forms.ValidationError("Debes tener al menos 18 años para registrarte.")
        return date_birth


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
                'placeholder': 'contraseña'
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
                    'placeholder': 'Correo Electrónico',
                    'class': 'form-control',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre Completo',
                    'class': 'form-control',
                }
            ),
            'ocupation': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'genero': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                },
            ),
        }

    def clean_date_birth(self):
        date_birth = self.cleaned_data.get("date_birth")
        if date_birth:
            today = date.today()
            age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))
            if age < 18:
                raise forms.ValidationError("El usuario debe tener al menos 18 años.")
        return date_birth

