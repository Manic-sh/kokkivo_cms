from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, Address
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput
    )

    first_name = forms.CharField(
        label='Name',
        widget=forms.TextInput
    )

    last_name = forms.CharField(
        label='Surname',
        widget=forms.TextInput
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        exclude = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise ValidationError(message)

        return password2

    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)

        # automatically set to email address to create a unique identifier
        instance.username = instance.email

        if commit:
            instance.save()

        return instance


class UserLoginForm(forms.Form):
    login_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['house_number_name', 'street', 'town', 'postcode']
