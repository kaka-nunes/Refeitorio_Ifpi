from django.contrib import messages
from django.shortcuts import redirect

from dining_hall.accounts.models import Servant, Student


class RedirectStudentMixin:

    redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(id=self.request.user.id)
            if student:
                return super().dispatch(request, *args, **kwargs)
        except:
            try:
                servant = Servant.objects.get(id=self.request.user.id)

                message = 'Ops, você não é estudante'
                messages.error(self.request, message)
                
                if servant:
                    return redirect('accounts:home')
            except:
                pass
        return redirect('admin:index')


class RedirectServantMixin:

    redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        try:
            servant = Servant.objects.get(id=self.request.user.id)
            
            if servant:
                return super().dispatch(request, *args, **kwargs)
        except:
            try:
                student = Student.objects.get(id=self.request.user.id)

                message = 'Ops, você não é servidor'
                messages.error(self.request, message)
                
                if student:
                    return redirect('accounts:home')
            except:
                pass
        return redirect('admin:index')