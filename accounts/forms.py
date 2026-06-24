from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomerProfile


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your username',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password',
        })


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'full_name',
            'phone',
            'address',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Choose a username',
            'email': 'you@example.com',
            'password1': 'Create a password',
            'password2': 'Re-enter your password',
            'full_name': 'Your full name',
            'phone': 'Phone number',
            'address': 'Your address (optional)',
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            CustomerProfile.objects.update_or_create(
                user=user,
                defaults={
                    'full_name': self.cleaned_data['full_name'],
                    'phone': self.cleaned_data['phone'],
                    'address': self.cleaned_data['address'],
                },
            )

        return user
