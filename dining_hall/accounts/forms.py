from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from dining_hall.accounts.models import Student, Servant


class StudantCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha', widget=forms.PasswordInput, required=True
    )
    password2 = forms.CharField(
        label='Confirmação de senha', widget=forms.PasswordInput,
        required=True
    )
    username = forms.CharField(label='Matrícula')

    class Meta:
        model = Student
        fields = [
            'username', 'name', 'email', 'entry_date', 'birthdate', 'cpf',
            'rg', 'phone', 'profilepic', 'student_class', 'password1',
            'password2'
        ]

    def clean_password2(self):
        """
        Check IF the password entries match.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não são iguais.")
        return password2

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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