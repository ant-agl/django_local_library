from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(label="Дата обновления",
                                   help_text="Введите дату между настоящим моментом и 4 неделями (по умолчанию 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(
                _('Недействительная дата - продление в прошлом'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Недействительная дата - продление более чем на 4 недели вперед'))

        return data


class NewUserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Повтроите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {'username': 'Имя пользователя', 'email': 'E-mail'}
        help_texts = {'username': ''}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
