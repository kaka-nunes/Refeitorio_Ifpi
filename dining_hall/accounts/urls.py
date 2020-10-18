from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from dining_hall.accounts import views

app_name = 'accounts'

urlpatterns = [
    path(
        'login/', LoginView.as_view(template_name='accounts/login.html'),
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
    path('historic/', views.HistoryStudentView.as_view(), name='historic'),
    path('pending/', views.PendingStudentView.as_view(), name='pending'),
    path('servant/', views.ServantHomeView.as_view(), name='servant'),
    path('add_student/', views.AddStudentView.as_view(), name='add_student'),
    path(
        'list_student/', views.ListStudentView.as_view(), name='list_student'
    ),
    path(
        'inative_student/<str:pk>', views.InativeStudentView.as_view(),
        name='inative_student'
    ),
    path(
        'edit_student/<str:pk>', views.UpdateStudentView.as_view(),
        name='edit_student'
    ),
    path('add_servant/', views.AddServantView.as_view(), name='add_servant'),
    path(
        'list_servant/', views.ListServantView.as_view(), name='list_servant'
    ),
    path(
        'inative_servant/<str:pk>', views.InativeServantView.as_view(),
        name='inative_servant'
    ),
    path(
        'edit_servant/<str:pk>', views.UpdateServantView.as_view(),
        name='edit_servant'
    ),
    path('add_food/', views.AddFoodView.as_view(), name='add_food'),
    path('list_food/', views.ListFoodView.as_view(), name='list_food'),
    path(
        'edit_food/<str:pk>', views.UpdateFoodView.as_view(), name='edit_food'
    ),
    path(
        'list_pending/', views.ListPendingView.as_view(), name='list_pending'
    ),
    path(
        'update_pass/', views.UserPasswordChangeView.as_view(),
        name='update_pass'
    ),
    path(
        'remove_pending/<str:pk>', views.RemovePendingView.as_view(),
        name='remove_pending'
    ),
]
