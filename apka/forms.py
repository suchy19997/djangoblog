from django import forms
from .models import Post, Profile # , KeepSafeUserModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(help_text="max 200 znaków")

    class Meta:
        model = Post
        fields = ['title', 'text', 'image']

# def clean_name(value):
#     data = value
#     print("data:",data)
#     existing = User.objects.filter(username=data).exists()
#     print("istnieje:",existing)
#     if existing:
#         raise forms.ValidationError("Name already in use")
#         print("działa")
#     return data

class SignUpForm(UserCreationForm):
    #username= forms.CharField(validators=[clean_name])
    first_name = forms.CharField(label="imię",max_length=100, required=False, help_text='nieobowiazkowe', widget=forms.TextInput(attrs={'placeholder': 'Imię', }))
    last_name = forms.CharField(label="Nazwisko",max_length=100,  required=False, help_text='nieobowiazkowe',widget=forms.TextInput(attrs={'placeholder': 'Nazwisko', }))
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
    def clean_username(self):
        data = self.cleaned_data.get('username')
        existing = User.objects.filter(username__iexact=data).exists()

        if existing:
            raise ValidationError('username', "Name already in use")
            self.add_error("username", "A user with this username already exists.")
            print("działa")
        return data
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(max_length=100, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Imię', 'class': 'form-control', }))
    last_name = forms.CharField(max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Nazwisko', 'class': 'form-control', }))


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']





class ProfileForm(forms.ModelForm):
    location = forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs={'placeholder': 'Miejscowość','class': 'form-control',}))
    birth_date = forms.DateField(required=False)
    class Meta:
        model = Profile
        fields = ( 'birth_date', 'location')
