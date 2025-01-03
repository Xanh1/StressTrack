from django.urls import path
from . import views

urlpatterns = [
    # general
    path('', views.home, name='home'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.log_out, name='logout'),

    # dashboard
    path('panel/', views.panel, name='panel'),
    path('tasks/', views.list_tasks, name='list-tasks'),
    path('tests/', views.list_tests, name='list-test'),
    path('course/', views.course, name='course'),

    # test
    path('test/<int:test_id>/', views.test, name = 'test'),

    # task
    path('tasks/update/<int:task_id>/', views.list_tasks, name='update-task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete-task'),
    
    # teams
    path('course/team/delete/<int:team_id>/', views.delete_team, name='delete-team'),
]