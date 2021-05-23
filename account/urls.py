from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/vacancies/', views.vacancies, name='vacancies'),
    path('profile/remove/<int:id>', views.remove, name='remove'),
    path('profile/decline/<int:cell_id>', views.decline, name='decline'),
    path('profile/vacation_accept/<int:cell_id>', views.vacation_accept, name='vacation_accept'),
    path('profile/accept/<int:id>', views.accept, name='accept')
]
