import uuid
from django.db import models

FOOD_CHOICES = [
    ("Café da manhã", "Café da manhã"),
    ("Almoço", "Almoço"),
    ("Jantar", "Jantar")
]


class Food(models.Model):
    id = models.UUIDField(
        "id da refeição", primary_key=True, default=uuid.uuid4, editable=False
    )
    description = models.CharField("decrição da refeição", max_length=255)
    date = models.DateField("data da refeição")
    limit_quantity = models.PositiveIntegerField("quantidade limite")
    type_food = models.CharField(
        "tipe de refeição", choices=FOOD_CHOICES, max_length=14
    )
    registered_user = models.ForeignKey(
        "accounts.Servant", verbose_name="usuário que cadastrou",
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    modified_at = models.DateTimeField('modificado em', auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'refeição'
        verbose_name_plural = 'refeições'


class Reservation(models.Model):
    id = models.UUIDField(
        "id da reserva", primary_key=True, default=uuid.uuid4, editable=False
    )
    date = models.DateField("data da reserva", auto_now_add=True)
    food = models.ForeignKey(
        "food.Food", verbose_name="refeição", on_delete=models.PROTECT
    )
    registered_user = models.ForeignKey(
        "accounts.Student", verbose_name="aluno que reservou",
        on_delete=models.PROTECT, related_name="student_reservation"
    )
    pending = models.BooleanField("pendente", default=True)
    pending_withdrawal_date = models.DateField(
        "data de retirada da pendência", null=True, blank=True
    )
    user_removed_pending = models.ForeignKey(
        "accounts.Servant", verbose_name="usuário que retirou a pendência",
        on_delete=models.PROTECT, null=True, blank=True
    )
    motive = models.CharField(
        'motivo da pendência', null=True, blank=True, max_length=255
    )
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    modified_at = models.DateTimeField('modificado em', auto_now=True)

    def __str__(self):
        return  self.food.type_food + " - " + str(self.registered_user) +\
            " - " + str(self.date.day) + "/" + str(self.date.month) + "/" +\
                str(self.date.year)

    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'