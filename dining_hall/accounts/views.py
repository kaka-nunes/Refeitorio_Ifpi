from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from dining_hall.accounts.forms import StudantCreateForm
from dining_hall.accounts.models import Servant, Student, User
from dining_hall.food.models import Food, Reservation


# @method_decorator(login_required, name='dispatch')
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
                login_message = 'Ops, faça login para acessar essa página'
                messages.error(self.request, login_message)
                return reverse_lazy('accounts:login')


@method_decorator(login_required, name='dispatch')
class StudentHomeView(TemplateView):
    template_name = "accounts/student_home.html"

    def get_context_data(self, **kwargs):
        context = super(StudentHomeView, self).get_context_data(**kwargs)
        context['page_name'] = 'home'
        lim_quant = 'Não disponível'
        reservations = 'Não disponível'
        available = 'Não disponível'
        type_food = ' - fora do horário de reservas'
        try:
            foods = Food.objects.filter(date=datetime.now())
            if datetime.now().hour <= 12:
                food = foods.get(type_food='Almoço')
                context['food'] = food
                lim_quant = food.limit_quantity
                if food.limit_quantity < 1:
                    lim_quant = 'Não disponível'
                type_food = ' - Almoço'
                reservations = str(Reservation.objects.filter(food=food).count())
            if datetime.now().hour >= 18:
                food = foods.get(type_food='Jantar')
                context['food'] = food
                lim_quant = food.limit_quantity
                if food.limit_quantity < 1:
                    lim_quant = 'Não disponível'
                type_food = ' - Jantar'
                reservations = Reservation.objects.filter(food=food).count()
                available = food.limit_quantity - reservations
        except:
            pass
        
        context['type_food'] = type_food
        context['reservations'] = reservations
        context['lim_quant'] = lim_quant
        context['available'] = available
        
        context['peding'] = Reservation.objects.filter(
            registered_user=self.request.user).count()
            
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
            messages.warning(self.request,
                'Ops, já existe reserva para essa refeição'
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
            food.limit_quantity += 1
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
class AddMotiveView(View):
    def post(self, *args, **kwargs):
        pk = self.request.POST.get('id_pending')
        reservation = Reservation.objects.get(id=pk)
        reservation.motive = self.request.POST.get('motive')
        reservation.save()
        message = 'Motivo adicionado com sucesso'
        messages.success(self.request, message)
        success_url = reverse_lazy('accounts:pending')
        return redirect(success_url)


@method_decorator(login_required, name='dispatch')
class ServantHomeView(TemplateView):
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
            if len(foods) > 0:
                food = foods.get(type_food=type_food)
                total_reservations = food[0].limit_quantity
                reservations = int(
                    Reservation.objects.filter(food=food).count())
                available = total_reservations - reservations
                context['type_food'] = str(food)
        except:
            pass
        pending = Reservation.objects.filter(pending=True).count
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