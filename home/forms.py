from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    catid=forms.IntegerField()


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,label='Kullanıcı Adı:')
    email = forms.EmailField(max_length=30,label='Email:')
    first_name=forms.CharField(max_length=30,label='Ad:')
    last_name=forms.CharField(max_length=30,label='Soyad:')

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')