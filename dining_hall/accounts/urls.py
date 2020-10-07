from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from dining_hall.accounts.views import (
    HomeRedirectView, StudentHomeView, ServantHomeView
)

app_name = 'accounts'

urlpatterns = [
    path(
        'login/', LoginView.as_view(template_name = 'accounts/login.html'),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', HomeRedirectView.as_view(), name='home'),
    path('student/', StudentHomeView.as_view(), name='student'),
    path('servant/', ServantHomeView.as_view(), name='servant'),
]