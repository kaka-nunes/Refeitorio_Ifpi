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
            'username', 'name', 'email', 'entry_date', 'profilepic', 'campus',
            'password1', 'password2'
        ]


class ServantUpdateForm(UserChangeForm):
    username = forms.CharField(label='SUAP', disabled=True)

    class Meta:
        model = Servant
        fields = [
            'username', 'name', 'email', 'entry_date', 'profilepic', 'campus'
        ]
    
    def __init__(self, *args, **kwargs):
        super(ServantUpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['entry_date'].widget.attrs['readonly'] = True