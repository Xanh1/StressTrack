from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Andy',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apolo',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    dni = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1103982731',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'ejemplo@unl.edu.ec',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '**********',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '**********',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'dni', 'email', 'password1', 'password2']

class CustomUserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Andy',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apolo',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    dni = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1103982731',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'ejemplo@unl.edu.ec',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'dni', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '**************',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '**************',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '**************',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']

class CustomAuthenticationForm(AuthenticationForm):
    
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'ejemplo@unl.edu.ec',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '**********',
        'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2'
    }))