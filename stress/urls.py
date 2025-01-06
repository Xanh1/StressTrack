from django.urls import path, re_path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView

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
    path('test/delete/<int:test_id>', views.delete_test, name = 'delete-test'),

    # task
    path('tasks/update/<int:task_id>/', views.list_tasks, name='update-task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete-task'),
    
    # teams
    path('course/team/delete/<int:team_id>/', views.delete_team, name='delete-team'),
    
    # reset password
    path('reset/password_reset', PasswordResetView.as_view(template_name='registration/password_reset_forms.html', email_template_name="registration/password_reset_emails.html"), name='password_reset'),
    path('reset/password_reset_done', PasswordResetDoneView.as_view(template_name='registration/password_reset_dones.html'), name = 'password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirms.html'), name = 'password_reset_confirm'),
    path('reset/done',PasswordResetCompleteView.as_view(template_name='registration/password_reset_completes.html') , name = 'password_reset_complete'),
    
    # pruebas
    path('prueba/', views.prueba, name='prueba'),
]