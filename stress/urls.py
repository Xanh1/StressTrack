from django.urls import path
from . import views

urlpatterns = [
    # general
    path('', views.home, name='home'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),

    # dashboard
    path('panel/', views.panel, name='panel'),
    path('tasks/', views.list_tasks, name='list-tasks'),
    path('tests/', views.list_tests, name='list-test'),
    path('course/', views.course, name='course'),
    
]