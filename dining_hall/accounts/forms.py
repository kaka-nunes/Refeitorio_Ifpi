from django import forms
from dining_hall.accounts.models import Student


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