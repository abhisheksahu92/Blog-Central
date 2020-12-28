from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=120, required=True)
    password = forms.CharField(label = 'Password', max_length=120, required=True,widget=forms.PasswordInput)
    email    = forms.EmailField(label = 'Email', required=True)
    confirm_email    = forms.EmailField(label = 'Confirm Email', required=True)
    first_name = forms.CharField(label = 'First Name', max_length=120, required=True)
    last_name = forms.CharField(label = 'Last Name', max_length=120, required=True)

    def clean(self,*args, **kwargs):
        print(self.cleaned_data)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email    = self.cleaned_data.get('email')
        confirm_email    = self.cleaned_data.get('confirm_email')
        
        if username and password:
            user = User.objects.filter(username=username).exists()
            if user:
                raise forms.ValidationError('Username registered. Please check with different username.')
        
        if email != confirm_email:
            raise forms.ValidationError('Emails and confirm email should be same.')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Emails already exists.')

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=120, required=True)
    password = forms.CharField(label = 'Password', max_length=120, required=True,widget=forms.PasswordInput)

    def clean(self,*args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = User.objects.filter(username=username).exists()
            if not user:
                raise forms.ValidationError('Username does not exists. Please register')
            user_pass = authenticate(username=username,password =password)
            if not user_pass:
                raise forms.ValidationError('Password is not correct.')
        