from django import forms
from .models import CustomUser, Course, Recommendation
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

class CustomUserCreationRoleForm(UserCreationForm):
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

    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'w-100 fs-7 py-2 px-2 bg-white border border-1 border-dark rounded-2'
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
        fields = ['first_name', 'last_name', 'dni', 'email', 'role', 'password1', 'password2']


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'teacher']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = self.fields['teacher'].queryset.filter(role='teacher')
        self.fields['teacher'].widget.attrs.update({
            'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2 bg-white',
            'placeholder': '',
        })

        self.fields['name'].widget.attrs.update({
            'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2',
            'placeholder': '',
        })


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['title', 'description', 'min_percent', 'max_percent']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalizar estilos de los campos
        self.fields['title'].widget.attrs.update({
            'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2',
            'placeholder': '',
        })

        self.fields['description'].widget.attrs.update({
            'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2',
            'placeholder': '',
        })

        self.fields['min_percent'].widget.attrs.update({
            'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2',
            'placeholder': '',
        })

        self.fields['max_percent'].widget.attrs.update({
            'class': 'w-100 fs-7 py-1 px-2 border border-1 border-dark rounded-2',
            'placeholder': '',
        })