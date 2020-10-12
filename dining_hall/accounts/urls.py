from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from dining_hall.accounts import views

app_name = 'accounts'

urlpatterns = [
    path(
        'login/', LoginView.as_view(
            template_name = 'accounts/login.html'
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.HomeRedirectView.as_view(), name='home'),
    path('student/', views.StudentHomeView.as_view(), name='student'),
    path(
        'add_reservation/', views.AddReservationView.as_view(),
        name='add_reservation'
    ),
    path(
        'cancel_reservation/', views.CancelReservationView.as_view(),
        name='cancel_reservation'
    ),
    path(
        'profile/<str:pk>', views.StudentProfileView.as_view(), name='profile'
    ),
    path(
        'historic/', views.HistoryStudentView.as_view(),
        name='historic'
    ),
    path(
        'pending/', views.PendingStudentView.as_view(),
        name='pending'
    ),
    path(
        'add_motive/', views.AddMotiveView.as_view(),
        name='add_motive'
    ),
    path('servant/', views.ServantHomeView.as_view(), name='servant'),
]