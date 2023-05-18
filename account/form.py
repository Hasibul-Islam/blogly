from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from .models import Profile

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user






class ProfileForm(forms.ModelForm):
    country = CountryField().formfield(attrs={'class': 'form-control huge'})
    profile_picture = forms.ImageField()
    class Meta:
        model = Profile
        fields = ('country', 'city', 'postal_code', 'phone', 'profile_picture', 'occupation', 'organization')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False
        self.fields['profile_picture'].widget.attrs['accept'] = 'image/*'
        self.instance.user = user
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Implement phone number validation logic if needed
        return phone

