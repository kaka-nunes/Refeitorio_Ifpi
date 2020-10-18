import os
import uuid

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string

from dining_hall.accounts.managers import UserManager


def profilepic_directory_path(instance, filename):
    name, extension = os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    file_name = get_random_string(10, chars)
    return 'profilepic/{0}/{1}{2}'.format(
        instance.id, file_name, extension
    )


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(
        "id do usuário", primary_key=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(
        'usuário (matricula para alunos e SUAP para servidores)',
        max_length=255, unique=True
    )
    name = models.CharField('nome', max_length=255)
    email = models.EmailField('e-mail', unique=True, null=True, blank=True)
    entry_date = models.DateField('data de ingresso', null=True, blank=True)
    profilepic = models.ImageField(
        verbose_name='foto', null=True, blank=True,
        upload_to=profilepic_directory_path
    )
    is_active = models.BooleanField('ativo', default=True)
    is_staff = models.BooleanField('equipe', default=False)
    is_admin = models.BooleanField('administrador', default=False)
    is_superuser = models.BooleanField('superuser', default=False)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    modified_at = models.DateTimeField('modificado em', auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'


class Servant(User):

    campus = models.ForeignKey(
        'course.Campus', on_delete=models.PROTECT, verbose_name='campus'
    )
    
    def save(self, *args, **kwargs):
        self.is_staff, self.is_admin, self.is_superuser = True, True, True
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'servidor'
        verbose_name_plural = 'servidores'


class Student(User):
    birthdate = models.DateField('data de nascimento')
    cpf = models.CharField('CPF', max_length=15, unique=True)
    rg = models.CharField('RG', max_length=20, unique=True)
    phone = models.CharField('telefone', max_length=14, unique=True)
    student_class = models.ForeignKey(
        'course.Class', on_delete=models.PROTECT, verbose_name='turma'
    )
    
    class Meta:
        verbose_name = 'aluno'
        verbose_name_plural = 'alunos'