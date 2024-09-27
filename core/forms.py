from django import forms
from django.forms import ModelForm
from .models import Producto, Profile
from django.contrib.auth.models import User, Group  # Importar el modelo User y Group 
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['SKU_PROD', 'NOMBRE_PROD', 'DESCRIPCION', 'PRECIO_PROD', 'CATEGORIA', 'IMAGEN', 'STOCK_PROD']

class UsuarioForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar contraseña")  # Campo para confirmar la contraseña

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not any(char.islower() for char in password):
            raise forms.ValidationError('La contraseña debe tener al menos una letra minúscula.')
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('La contraseña debe tener al menos una letra mayúscula.')
        if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/" for char in password):
            raise forms.ValidationError('La contraseña debe tener al menos un carácter especial.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Encripta la contraseña
        if commit:
            user.save()
            grupo = self.cleaned_data['grupo']
            user.groups.add(grupo)  # Asigna el grupo seleccionado al usuario
        return user
 
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Categoría o Grupo")  # Nuevo campo de grupo

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']  # Añadimos 'group' a los campos

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")
        return email
    

class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user    