from datetime import datetime
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from dining_hall.accounts.forms import (
    StudantCreateForm, ServantCreateForm, ServantUpdateForm,
    ConfirmReservationForm
)
from dining_hall.accounts.mixins import (
    RedirectStudentMixin, RedirectServantMixin
)
from dining_hall.accounts.models import Servant, Student, User
from dining_hall.food.models import Food, Reservation
from dining_hall.food.forms import FoodAddForm, PendingRemoveForm



@method_decorator(login_required, name='dispatch')
class HomeRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        try: 
            student = Student.objects.get(id=self.request.user.id)
            if student:
                return reverse_lazy('accounts:student')
        except:
            try:
                servant = Servant.objects.get(id=self.request.user.id)
                if servant:
                    return reverse_lazy('accounts:servant')
            except:
                if self.request.user.id:
                    return reverse_lazy('admin:index')
                login_message = 'Ops, faça login para acessar essa página'
                messages.error(self.request, login_message)
                return reverse_lazy('accounts:login')


@method_decorator(login_required, name='dispatch')
class StudentHomeView(RedirectStudentMixin, TemplateView):
    template_name = "accounts/student_home.html"

    def get_context_data(self, **kwargs):
        context = super(StudentHomeView, self).get_context_data(**kwargs)
        context['page_name'] = 'home'
        lim_quant = 'Não disponível'
        total_quant = 'Não disponível'
        reservations = 'Não disponível'
        available = 'Não disponível'
        type_food = ' - fora do horário de reservas'
        try:
            foods = Food.objects.filter(date=datetime.now())
            if datetime.now().hour <= 12:
                food = foods.get(type_food='Almoço')
                context['food'] = food
                lim_quant = food.limit_quantity
                total_quant = food.total_quantity
                if food.limit_quantity < 1:
                    lim_quant = 'Não disponível'
                type_food = ' - Almoço'
                reservations = Reservation.objects.filter(food=food).count()
            if datetime.now().hour >= 18:
                type_food = ' - Jantar'
                food = foods.get(type_food='Jantar')
                context['food'] = food
                lim_quant = food.limit_quantity
                total_quant = food.total_quantity
                if food.limit_quantity < 1:
                    lim_quant = 'Não disponível'
                reservations = Reservation.objects.filter(food=food).count()
                lim_quant = food.total_quant - reservations
        except:
            pass
        if datetime.now().hour > 10 and datetime.now().hour < 14 or \
                datetime.now().hour > 23:
            context['reservation_unavailable'] = True
        context['total_quant'] = total_quant
        context['type_food'] = type_food
        context['reservations'] = reservations
        context['lim_quant'] = lim_quant
        context['available'] = available
        context['peding'] = Reservation.objects.filter(
            registered_user=self.request.user
        ).filter(pending=True).count()
        context["student"] = Student.objects.get(id=self.request.user.id)
        return context


@method_decorator(login_required, name='dispatch')
class AddReservationView(View):

    def get(self, *args, **kwargs):
        foods = Food.objects.filter(date=datetime.now())
        if datetime.now().hour <= 12:
            food = foods.get(type_food='Almoço')
        if datetime.now().hour >= 18:
            food = foods.get(type_food='Jantar')
        student = Student.objects.get(id=self.request.user.id)
        reservations = Reservation.objects.filter(date=datetime.now()).filter(
            registered_user=student).filter(food=food)
        if(len(reservations)) >= 1:
            messages.warning(
                self.request, 'Ops, já existe reserva para essa refeição'
            )
            return redirect(reverse_lazy('accounts:home'))
        reservation = Reservation.objects.create(
            date=datetime.now(), food=food,
            registered_user=student
        )
        food.limit_quantity = food.limit_quantity - 1
        food.save()
        reservation.save()
        messages.success(self.request, 'Reserva feita com sucesso!')
        return redirect(reverse_lazy('accounts:home'))


@method_decorator(login_required, name='dispatch')
class CancelReservationView(View):

    def get(self, *args, **kwargs):
        foods = Food.objects.filter(date=datetime.now())
        if datetime.now().hour <= 12:
            try:
                food = foods.get(type_food='Almoço')
            except Food.DoesNotExist:
                pass
        if datetime.now().hour >= 18:
            try:
                food = foods.get(type_food='Jantar')
            except Food.DoesNotExist:
                pass
        student = Student.objects.get(id=self.request.user.id)
        reservations = Reservation.objects.filter(date=datetime.now()).filter(
            registered_user=student).filter(food=food)
        if(len(reservations)) >= 1:
            messages.success(self.request, 'Reserva cancelada com sucesso')
            reservations[0].delete()
            food.limit_quantity = food.limit_quantity + 1
            food.save()
            return redirect(reverse_lazy('accounts:home'))
        else:
            messages.warning(
                self.request, 'Não há reserva do aluno a ser cancelada'
            )
            return redirect(reverse_lazy('accounts:home'))


@method_decorator(login_required, name='dispatch')
class HistoryStudentView(ListView):
    template_name = "accounts/history_student.html"

    def get_queryset(self):
        queryset = Reservation.objects.filter(
            registered_user__id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HistoryStudentView, self).get_context_data(**kwargs)
        context['page_name'] = 'history'
        return context


@method_decorator(login_required, name='dispatch')
class PendingStudentView(ListView):
    template_name = "accounts/pending_student.html"

    def get_queryset(self):
        queryset = Reservation.objects.filter(
            registered_user__id=self.request.user.id).filter(pending=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PendingStudentView, self).get_context_data(**kwargs)
        context['page_name'] = 'peding'
        return context


@method_decorator(login_required, name='dispatch')
class StudentProfileView(DetailView):
    model = Student
    template_name = "accounts/student_profile.html"

    def get_context_data(self, **kwargs):
        context = super(StudentProfileView, self).get_context_data(**kwargs)
        context['page_name'] = 'profile'
        return context


@method_decorator(login_required, name='dispatch')
class ServantHomeView(RedirectServantMixin, TemplateView):
    template_name = "accounts/servant_home.html"

    def get_context_data(self, **kwargs):
        context = super(ServantHomeView, self).get_context_data(**kwargs)
        today = datetime.now()
        context['page_name'] = 'home'
        type_food = 'Almoço'
        context['type_food'] = 'Não disponível'
        total_reservations = 0
        reservations = 0
        available = 0
        if today.hour > 12:
            type_food = 'Jantar'
        try:
            foods = Food.objects.filter(date=today)
            if foods.count() >= 1:
                food = foods.get(type_food=type_food)
                total_reservations = food.total_quantity
                reservations = Reservation.objects.filter(food=food).count()
                available = total_reservations - reservations
                context['type_food'] = str(food)
        except:
            pass
        pending = Reservation.objects.filter(pending=True).count()
        context['peding'] = pending
        context['available'] = available
        context['reservations'] = reservations
        context['total_reservations'] = total_reservations
        context['page_name'] = 'home'
        context["servant"] = Servant.objects.get(id=self.request.user.id)
        return context


class AddStudentView(SuccessMessageMixin, CreateView):
    model = Student
    template_name = 'accounts/add_student.html'
    form_class = StudantCreateForm
    success_url = reverse_lazy('accounts:add_student')
    success_message = 'Aluno adicionado com sucesso'

    def get_context_data(self, **kwargs):
        context = super(AddStudentView, self).get_context_data(**kwargs)
        context['page_name'] = 'student'
        context['action'] = 'Cadastrar'
        return context


@method_decorator(login_required, name='dispatch')
class ListStudentView(ListView):
    model = Student
    template_name = "accounts/list_student.html"

    def get_queryset(self):
        queryset = Student.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListStudentView, self).get_context_data(**kwargs)
        context['page_name'] = 'student'
        return context


@method_decorator(login_required, name='dispatch')
class InativeStudentView(View):

    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        action = 'desativado'
        if student.is_active:
            student.is_active = False
        else:
            action = 'ativado'
            student.is_active = True
        student.save()
        message = 'Aluno ' + action + ' com sucesso'
        messages.success(request, message)
        success_url = reverse_lazy('accounts:list_student')
        return redirect(success_url)


class UpdateStudentView(SuccessMessageMixin, UpdateView):
    model = Student
    template_name = 'accounts/add_student.html'
    form_class = StudantCreateForm
    success_url = reverse_lazy('accounts:list_student')
    success_message = 'Aluno alterado com sucesso'

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        context['page_name'] = 'student'
        context['action'] = 'Alterar'
        return context


class RemovePendingView(SuccessMessageMixin, UpdateView):
    model = Reservation
    template_name = 'accounts/remove_pending.html'
    form_class = PendingRemoveForm
    success_url = reverse_lazy('accounts:list_pending')

    def get_context_data(self, **kwargs):
        context = super(RemovePendingView, self).get_context_data(**kwargs)
        context['page_name'] = 'pending'
        return context

    def form_valid(self, form):
        reservation = form.save(commit=False)
        servant = Servant.objects.get(pk=self.request.user.pk)
        reservation.user_removed_pending = servant
        reservation.pending_withdrawal_date = datetime.now()
        reservation.pending = False
        reservation.save()
        message = 'Pendência retirada com sucesso'
        messages.success(self.request, message)
        return redirect(self.success_url)


class AddServantView(SuccessMessageMixin, CreateView):
    model = Servant
    template_name = 'accounts/add_servant.html'
    form_class = ServantCreateForm
    success_url = reverse_lazy('accounts:add_servant')
    success_message = 'Servidor adicionado com sucesso'

    def get_context_data(self, **kwargs):
        context = super(AddServantView, self).get_context_data(**kwargs)
        context['page_name'] = 'servant'
        context['action'] = 'Cadastrar'
        return context


@method_decorator(login_required, name='dispatch')
class ListServantView(ListView):
    model = Servant
    template_name = "accounts/list_servant.html"

    def get_queryset(self):
        queryset = Servant.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListServantView, self).get_context_data(**kwargs)
        context['page_name'] = 'servant'
        return context


@method_decorator(login_required, name='dispatch')
class InativeServantView(View):

    def get(self, request, pk):
        success_url = reverse_lazy('accounts:list_servant')
        servant1 = Servant.objects.get(pk=pk)
        servant2 = Servant.objects.get(pk=self.request.user.id)
        if servant1 == servant2:
            message = 'Ops, você não pode se desativar!'
            messages.error(request, message)
            return redirect(success_url)

        servant = Servant.objects.get(pk=pk)
        action = 'desativado'
        if servant.is_active:
            servant.is_active = False
        else:
            action = 'ativado'
            servant.is_active = True
        servant.save()
        message = 'Servidor ' + action + ' com sucesso'
        messages.success(request, message)
        return redirect(success_url)


class UpdateServantView(SuccessMessageMixin, UpdateView):
    model = Servant
    template_name = 'accounts/add_servant.html'
    form_class = ServantUpdateForm
    success_url = reverse_lazy('accounts:list_servant')
    success_message = 'Servidor alterado com sucesso'

    def get_context_data(self, **kwargs):
        context = super(UpdateServantView, self).get_context_data(**kwargs)
        context['page_name'] = 'servant'
        if str(self.request.user.id) == str(self.kwargs['pk']):
            context['page_name'] = 'profile'
        context['action'] = 'Alterar'
        return context


class AddFoodView(SuccessMessageMixin, CreateView):
    model = Food
    template_name = 'accounts/add_food.html'
    form_class = FoodAddForm
    success_url = reverse_lazy('accounts:add_food')

    def form_valid(self, form):
        food = form.save(commit=False)
        servant = Servant.objects.get(pk=self.request.user.pk)
        food.registered_user = servant
        food.save()
        message = 'Refeição adicionado com sucesso'
        messages.success(self.request, message)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(AddFoodView, self).get_context_data(**kwargs)
        context['page_name'] = 'food'
        context['action'] = 'Cadastrar'
        return context


@method_decorator(login_required, name='dispatch')
class ListFoodView(ListView):
    model = Food
    template_name = "accounts/list_food.html"

    def get_queryset(self):
        queryset = Food.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListFoodView, self).get_context_data(**kwargs)
        context['page_name'] = 'food'
        return context


class UpdateFoodView(SuccessMessageMixin, UpdateView):
    model = Food
    template_name = 'accounts/add_food.html'
    form_class = FoodAddForm
    success_url = reverse_lazy('accounts:list_food')
    success_message = 'Refeição alterada com sucesso'

    def form_valid(self, form):
        food = form.save(commit=False)
        servant = Servant.objects.get(pk=self.request.user.pk)
        food.registered_user = servant
        food.save()
        message = 'Refeição alterada com sucesso'
        messages.success(self.request, message)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(UpdateFoodView, self).get_context_data(**kwargs)
        context['page_name'] = 'food'
        context['action'] = 'Alterar'
        return context


@method_decorator(login_required, name='dispatch')
class ListPendingView(ListView):
    model = Food
    template_name = "accounts/list_pending.html"

    def get_queryset(self):
        q1 = Reservation.objects.filter(pending=True)
        q2 = Reservation.objects.exclude(pending_withdrawal_date=None)
        queryset = list(chain(q1, q2))
        return q1

    def get_context_data(self, **kwargs):
        context = super(ListPendingView, self).get_context_data(**kwargs)
        context['page_name'] = 'pending'
        return context


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/update_pass.html'
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        messages.success(self.request, 'Senha alterada com sucesso')
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(
            UserPasswordChangeView, self).get_context_data(**kwargs)
        context['page_name'] = 'profile'
        try:
            student = Student.objects.get(id=self.request.user.id)
            if student:
                context['template_base'] = "base.html"
        except:
            context['template_base'] = "base_servant.html"
        return context


class ConfirmReservationView(SuccessMessageMixin, TemplateView):
    template_name = 'accounts/reservations.html'

    def post(self, *args, **kwargs):
        today = datetime.now()
        type_food = 'Almoço'
        if today.hour > 14:
            type_food = 'Jantar'
        try:
            foods = Food.objects.filter(date=today)
            if foods.count() >= 1:
                food = foods.get(type_food=type_food)
                user = Student.objects.get(
                    username=self.request.POST['username']
                )
                reservation = Reservation.objects.get(
                    food=food, registered_user=user
                )
                message = "Pendência retirada"
                if reservation.pending == False:
                    message = "Pendência já retirada"
                    messages.warning(self.request, message)
                else:
                    reservation.pending = False
                    reservation.save()
                    messages.success(self.request, message)
        except:
            messages.error(self.request, "Reserva não encontrada")

        return redirect(reverse_lazy('accounts:confirm_reservation'))
