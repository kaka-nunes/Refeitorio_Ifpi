from django import forms


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label='Nome de usuário (matrícula para alunos e SUAP para servidores',
        max_length=255
    )
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)