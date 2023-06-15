from django import forms
from django.contrib.auth.models import User
from .models import Publicacion, Usuario
from django.db import models
from django.contrib.auth.forms import UserChangeForm
 
class RegistrarForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Confirm Password')
    email = forms.EmailField(label='Email')
    profile_image = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'profile_image')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
class PublicacionForm(forms.ModelForm):
    titulo = forms.CharField(label='Titulo', widget=forms.TextInput(attrs={'class': 'centered-input'}))
    cuerpo = forms.CharField(label='Cuerpo', widget=forms.TextInput(attrs={'class': 'centered-input'}))
    imagen_portada = forms.ImageField(label='Imagen portada', required=False)
    class Meta:
        model = Publicacion
        fields = ['titulo', 'cuerpo', 'imagen_portada']

class PerfilUsuarioForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'image_profile')
