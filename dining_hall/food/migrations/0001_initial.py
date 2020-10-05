# Generated by Django 3.1.2 on 2020-10-05 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id da refeição')),
                ('description', models.CharField(max_length=255, verbose_name='decrição da refeição')),
                ('date', models.DateField(verbose_name='data da refeição')),
                ('limit_quantity', models.PositiveIntegerField(verbose_name='quantidade limite')),
                ('type_food', models.CharField(choices=[('Café da manhã', 'Café da manhã'), ('Almoço', 'Almoço'), ('Jantar', 'Jantar')], max_length=14, verbose_name='tipe de refeição')),
                ('registered_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='usuário que cadastrou')),
            ],
            options={
                'verbose_name': 'refeição',
                'verbose_name_plural': 'refeições',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id da reserva')),
                ('date', models.DateField(auto_now_add=True, verbose_name='data da reserva')),
                ('pending', models.BooleanField(default=True, verbose_name='pendente')),
                ('pending_withdrawal_date', models.DateField(blank=True, null=True, verbose_name='data de retirada da pendência')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='food.food', verbose_name='refeição')),
                ('registered_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='student_reservation', to='accounts.student', verbose_name='aluno que reservou')),
                ('user_removed_pending', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='usuário que retirou a pendência')),
            ],
            options={
                'verbose_name': 'reserva',
                'verbose_name_plural': 'reservas',
            },
        ),
    ]
