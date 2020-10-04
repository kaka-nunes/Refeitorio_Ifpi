# Importações Python
import uuid
# Importações Django
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
# Importações da aplicação
from refeitorio.accounts.managers import UserManager


SEX_CHOICES = [
    ('M', 'masculino'),
    ('F', 'feminino')
]

class User(AbstractUser, PermissionsMixin):
    """
    Model customizado do usuário base
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField('matricula', max_length=255, unique=True)
    name = models.CharField('nome', max_length=255)
    sex = models.CharField('sexo', max_length=9, choices=SEX_CHOICES)
    email = models.EmailField('e-mail', unique=True, null=True, blank=True)
    is_active = models.BooleanField('ativo', default=False)
    is_staff = models.BooleanField('equipe', default=False)
    is_admin = models.BooleanField('administrador', default=False)
    is_superuser = models.BooleanField('superuser', default=False)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    modified_at = models.DateTimeField('modificado em', auto_now=True)

    REQUIRED_FIELDS = ['name']

    # Manager Object
    objects = UserManager()

    def __str__(self):
        """
        Retona o nome do usuário como identificador da aplicação
        """
        return self.name

    class Meta:
        """
        Model Meta class.
        Define o nome que será exibido como model
        """
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'
