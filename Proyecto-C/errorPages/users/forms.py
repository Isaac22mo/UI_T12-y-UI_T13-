from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel',
                  'password1', 'password2']
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico',
                    'required': True,
                    'pattern': '^[0-9]{5}tn[0-9]{3}@utez\.edu\.mx$'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre completo',
                    'required': True,
                }
            ),
            'surname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su apellido',
                    'required': True,
                }
            ),
            'control_number': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su número de control',
                    'required': True,
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su edad',
                    'required': True,
                }
            ),
            'tel': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su número telefónico',
                    'required': True,
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su contraseña',
                    'required': True,
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Confirme su contraseña',
                    'required': True,
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match(r'^[0-9]{5}tn[0-9]{3}@utez\.edu\.mx$', email):
            raise ValidationError("El correo debe tener el formato correcto: 12345tn123@utez.edu.mx")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email
    
    def clean_control_number(self):
        control_number = self.cleaned_data.get("control_number")
        if not re.match(r'^[0-9]{5}tn[0-9]{3}$', control_number):
            raise ValidationError("El número de control debe tener el formato correcto: 12345tn123")
        return control_number
    
    def clean_tel(self):
        tel = self.cleaned_data.get("tel")
        if len(str(tel)) != 10:
            raise ValidationError("El número telefónico debe tener 10 dígitos.")
        return tel


    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise ValidationError("La contraseña debe contener al menos 8 caracteres.")
        if not re.search(r'[!#$%&?]', password):
            raise ValidationError("La contraseña debe contener al menos un símbolo (!, #, $, %, & o ?).")
        if not re.search(r'\d', password):
            raise ValidationError("La contraseña debe contener al menos un número.")
        return password

    # def clean_control_number(self):
    #     control_number = self.cleaned_data.get("control_number")
    #     if len(str(control_number)) != 10:
    #         raise ValidationError("El número de control debe tener exactamente 10 caracteres.")
    #     return control_number

class CustomUserLoginForm(AuthenticationForm):
    email = forms.CharField(
        label="Correo electrónico",
        max_length=150
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")

        return cleaned_data