from django import forms


class AuthForm(forms.Form):
    email = forms.EmailField(widget=(
        forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите Вашу почту',
            'id': 'email'
        })
    ))
    password = forms.CharField(widget=(
        forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите код подтверждения',
            'id': 'password',
            'hidden': True
        })
    ))
