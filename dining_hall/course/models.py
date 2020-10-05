import uuid
from django.db import models


SHIFT_CHOICES = [
    ('matutino', 'matutino'),
    ('vespertino', 'vespertino'),
    ('noturno', 'noturno')
]

class Course(models.Model):
    id = models.UUIDField(
        "id do curso", primary_key=True, default=uuid.uuid4, editable=False
    )
    description = models.CharField('descrição', max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'


class Class(models.Model):
    id = models.UUIDField(
        "id da turma", primary_key=True, default=uuid.uuid4, editable=False
    )
    course = models.ForeignKey(
        'course.Course', on_delete=models.PROTECT, verbose_name='curso'
    )
    shift = models.CharField('turno', choices=SHIFT_CHOICES, max_length=10)
    description = models.CharField('descrição', max_length=55)
    def __str__(self):
        return self.description + ' - ' + str(self.course) + ' - ' + self.shift

    class Meta:
        verbose_name = 'turma'
        verbose_name_plural = 'turmas'
