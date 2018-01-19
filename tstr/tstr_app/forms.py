# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm


class CustomizedPasswordChange(PasswordChangeForm):
    """Translated to polish form to change user password"""
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': ("Stare hasło niepoprawne. "
                               "Spróbuj ponownie."),
        'password_mismatch': ("Hasła nie są identyczne."),

    })
    old_password = forms.CharField(label=("Stare hasło"),
                                   widget=forms.PasswordInput(attrs={'class':"input-lg form-control"})
                                   )

    new_password1 = forms.CharField(label=("Nowe hasło"),
                                    widget=forms.PasswordInput(attrs={'class':"input-lg form-control"}))
    new_password2 = forms.CharField(label=("Powtórz nowe hasło"),
                                    widget=forms.PasswordInput(attrs={'class':"input-lg form-control"}))

