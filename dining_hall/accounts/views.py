from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView, TemplateView

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
        foods = Food.objects.filter(date=datetime.now())
        if datetime.now().hour == 12:
            food = foods.get(type_food='Almoço')
            context['food'] = food
            context['lim_quant'] = food.limit_quantity
            context['type_food'] = ' - Almoço'
            reservations = str(Reservation.objects.filter(food=food).count())
            context['reservations'] = reservations
        if datetime.now().hour > 0:
            food = foods.get(type_food='Jantar')
            context['food'] = food
            context['lim_quant'] = food.limit_quantity
            context['type_food'] = ' - Jantar'
            reservations = Reservation.objects.filter(food=food).count()
            context['reservations'] = reservations
            context['available'] = food.limit_quantity - reservations
        else:
            context['lim_quant'] = 'Não disponível'
            context['type_food'] = ' - fora do horário de reservas'
        
        context['peding'] = Reservation.objects.filter(
            registered_user=self.request.user).count()
            
        context["student"] = Student.objects.get(id=self.request.user.id)
        return context

@method_decorator(login_required, name='dispatch')
class ServantHomeView(TemplateView):
    template_name = "accounts/servant_home.html"
            
