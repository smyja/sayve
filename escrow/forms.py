from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from . import models
from .models import User,sendcoin


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, help_text='First Name', required=False)
    last_name = forms.CharField(max_length=100, help_text='Last Name', required=False)

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'placeholder': ('Email'), 'class': 'log'})


        self.fields['password1'].widget.attrs.update(
            {'placeholder': ('Password'), 'class': 'log swiy'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': ('Confirm password'), 'class': 'log swiy'}) 
    class Meta:
        model = User
        
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)
        widgets = {'first_name': forms.HiddenInput(),'last_name': forms.HiddenInput()}
        
    
    def clean_email(self):
        
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError('This email is already in use! Try another email.')
        return email


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)



    class Meta:
        model = User
        fields = ('email', 'first_name','last_name', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )

    class Meta:
        model = User
        fields = '__all__'
      

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class TransferForm(forms.ModelForm):
   
    sender = forms.CharField(help_text="Your username")

    class Meta:
        model = sendcoin
        fields = [
            "sender",
            "receiver", 
            "amount"
            
        ]