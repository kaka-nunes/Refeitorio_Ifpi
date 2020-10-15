from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from dining_hall.accounts.models import Student, Servant


class StudantCreateForm(forms.ModelForm):
    username = forms.CharField(label='Matrícula')
    class Meta:
        model = Student
        fields = [
            'username', 'name', 'email', 'entry_date', 'birthdate', 'cpf',
            'rg', 'phone', 'profilepic', 'student_class'
        ]


class AddMotivePendingForm(forms.Form):
    motive = forms.CharField(label='Motivo')


class ServantCreateForm(UserCreationForm):
    username = forms.CharField(label='SUAP')
    class Meta:
        model = Servant
        fields = [
            'username', 'name', 'email', 'entry_date', 'profilepic',
            'password1', 'password2'
        ]


class ServantUpdateForm(UserChangeForm):
    username = forms.CharField(label='SUAP')
    class Meta:
        model = Servant
        fields = [
            'username', 'name', 'email', 'entry_date', 'profilepic',
        ]