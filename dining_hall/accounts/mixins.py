"""
from django.shortcuts import redirect


class RedirectStudentyMixin:

    def get(self, *args, **kwargs):
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
"""