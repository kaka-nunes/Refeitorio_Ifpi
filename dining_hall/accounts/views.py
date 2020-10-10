from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic import CreateView, DetailView

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
        foods = Food.objects.filter(date=datetime.now())
        lim_quant = 'Não disponível'
        reservations = 'Não disponível'
        available = 'Não disponível'
        type_food = ' - fora do horário de reservas'
        if datetime.now().hour <= 12:
            food = foods.get(type_food='Almoço')
            context['food'] = food
            lim_quant = food.limit_quantity
            type_food = ' - Almoço'
            reservations = str(Reservation.objects.filter(food=food).count())
        if datetime.now().hour <= 18:
            food = foods.get(type_food='Jantar')
            context['food'] = food
            lim_quant = food.limit_quantity
            type_food = ' - Jantar'
            reservations = Reservation.objects.filter(food=food).count()
            available = food.limit_quantity - reservations
        
        context['type_food'] = type_food
        context['reservations'] = reservations
        context['lim_quant'] = lim_quant
        context['available'] = available
        
        context['peding'] = Reservation.objects.filter(
            registered_user=self.request.user).count()
            
        context["student"] = Student.objects.get(id=self.request.user.id)
        return context

@method_decorator(login_required, name='dispatch')
class ServantHomeView(TemplateView):
    template_name = "accounts/servant_home.html"


@method_decorator(login_required, name='dispatch')
class StudentProfileView(DetailView):
    model = Student
    template_name = "accounts/student_profile.html"
    
    def get_context_data(self, **kwargs):
        context = super(StudentProfileView, self).get_context_data(**kwargs)
        context['page_name'] = 'profile'
        return context
