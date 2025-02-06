from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm, CustomPasswordChangeForm, CustomUserCreationRoleForm, CreateCourseForm, RecommendationForm
from .models import TestResult, Test, Option, Answer, Task, Team, CustomUser, Question, Notification, Course, Recommendation
from django.contrib.auth.decorators import login_required
from .utils import test_resolve
from django.db.models import Avg
from datetime import date

def home(request):
    if request.user.is_authenticated:
        return redirect('panel')
    return render(request, 'index.html')

def log_in(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        user = CustomUser.objects.filter(email=request.POST.get('username')).first()
        
        if not user:
            messages.error(request, "Credenciales incorrectas. Inténtalo de nuevo")
            return redirect('login')

        if user.is_active == False:
            messages.error(request, "Tu cuenta está inactiva. Contacta al administrador")
            return redirect('login') 

        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('panel')
        else:
            messages.error(request, "Credenciales incorrectas. Inténtalo de nuevo")
            return redirect('login')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('panel')

    return render(request, 'register.html', {'form': form})

@login_required
def panel(request):
    user = request.user

    course = user.course
    team = user.group
    tasks = None
    tests = None
    top_3_stressed_students = None
    average_stress = None
    course_teaching = user.teaching_courses.first()
    courses = Course.objects.all()
    professors = CustomUser.objects.filter(role='teacher').all()

    if course_teaching:
        students = course_teaching.students.filter(stress__gt=0) 
        top_3_stressed_students = students.order_by('-stress')[:3]
        average_stress = int(students.aggregate(avg_stress=Avg('stress'))['avg_stress'] or 0)

    if course:
        tasks = course.tasks.filter(due_date__gte=date.today()).order_by('due_date')

    if team:
        tests = team.tests.all()

    stress = user.stress
    color = ""
    
    recommendations = user.recommendation

    if 0 <= stress <= 20:
        color = 'bg-good'
    elif 20 < stress <= 40:
        color = 'bg-not-bad'
    elif 40 < stress <= 60:
        color = 'bg-dangerr'
    elif 60 < stress <= 100:
        color = 'bg-dying'
    
    context = {
        'name': user.first_name or "Usuario",
        'color': color,
        'recommendation': recommendations,
        'stress': stress,
        'role': user.role,
        'top_3_stressed_students': top_3_stressed_students,
        'average_stress': average_stress,
        'course_teaching': course_teaching,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
        'courses': courses,
        'professors': professors,
    }

    if tasks:
        if tasks.exists():
            tmp_task = tasks.first()
            task = {
                'title': tmp_task.title,
                'date': tmp_task.due_date
            }
        else:
            task = None
    else:
        task = None

    if tests:
        tmp_test = tests.last()
        flg = test_resolve(tmp_test, user)
        test = {
            'id': tmp_test.id,
            'title': tmp_test.title,
            'state': flg
        }
    else:
        test = None

    context['task'] = task
    context['test'] = test
    
    return render(request, 'dashboard/panel.html', context)

@login_required
def list_tasks(request):

    user = request.user

    if request.method == 'POST':

        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        course = user.teaching_courses.first()

        if 'form-update' in request.POST:
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id, course=course)
            
            task.title = title
            task.due_date = due_date
            task.save()
            
            messages.success(request, "La tarea se ha actualizado satisfactoriamente")
            return redirect('list-tasks')
        else:
            msg, task = create_task(title, due_date, course)
            if task:
                notify(request, course.students.all(), f'Se asignado una nueva tarea: {task.title}', 'list-tasks')
            messages.success(request, msg)
            return redirect('list-tasks')

    if user.role == 'student':
        course = user.course
    else:
        course = user.teaching_courses.first()

    if course:
        tasks = course.tasks.all()
    else:
        tasks = None
    
    context = {
        'tasks': tasks,
        'role': user.role,
        'course': course,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
    }

    return render(request, 'dashboard/task.html', context)

@login_required
def list_tests(request):

    user = request.user

    team = user.group

    if request.method == 'POST':
        if 'assign-test-form' in request.POST:
            test_id = request.POST.get('test-id')
            teams_id = request.POST.getlist('groups[]')
            
            test = get_object_or_404(Test, id=test_id)
            teams = Team.objects.filter(id__in=teams_id)
            
            test.Team.set(teams)
            test.save()

            students = set()
    
            for team in teams:
                students.update(team.members.all())

            notify(request, users=students, message='Se agregado un nuevo test', url='list-test')

            messages.success(request, "Se ha asignado el test correctamente")
            return redirect('list-test')
        
        elif 'assign-test-form-user' in request.POST:

            test_id = request.POST.get('test-id')
            test = get_object_or_404(Test, id=test_id)

            selected_student_ids = request.POST.getlist('students[]')

            selected_students = CustomUser.objects.filter(id__in=selected_student_ids)

            for student in CustomUser.objects.all():
                student.tests.remove(test)

            for student in selected_students:
                student.tests.add(test)

            notify(request, users=selected_students, message='Se agregado un nuevo test', url='list-test')
            messages.success(request, "Test asignado/desasignado correctamente.")

            return redirect('list-test')
        
        elif 'assign-test-form-all' in request.POST:
            is_checked = 'course-form' in request.POST
    
            test_id = request.POST.get('test-id')
            test = get_object_or_404(Test, id=test_id)

            course = user.teaching_courses.first()

            students = course.students.all()

            if is_checked:
                for student in students:
                    student.tests.add(test)
                notify(request, users=students, message='Se agregado un nuevo test', url='list-test')
                messages.success(request, "Se ha asignado el test correctamente")
            else:
                for student in students:
                    student.tests.remove(test)
                messages.success(request, "Se ha desasignado el test correctamente")

            return redirect('list-test')
        
        elif 'edit-test-form' in request.POST:
            test_id = request.POST.get('test-id')
            test_title = request.POST.get('title')
            test = get_object_or_404(Test, id=test_id)

            test.title = test_title
            test.save()

            test.questions.all().delete()
            questions = request.POST.getlist('questions[]')

            for question_text in questions:
                if question_text.strip():
                    Question.objects.create(description=question_text, test=test)

            messages.success(request, 'Se ha actualizado el test correctamente')
            return redirect('list-test')        
        else:
            test_name = request.POST.get('title')
            course = user.teaching_courses.first()
            test = Test.objects.create(title=test_name, course=course)

            questions = request.POST.getlist('questions[]')

            for question_text in questions:
                if question_text.strip():
                    Question.objects.create(description=question_text, test=test)
            
            messages.success(request, 'Se ha creado el test')
            return redirect('list-test')
    
    if team:
        tests_group = team.tests.all()
    else:
        tests_group = None
    
    tests_user = user.tests.all()

    if tests_group:
        tests = tests_group.union(tests_user)
    else:
        tests = tests_user

    list_test = []

    if tests:
        for test in tests:
            answered = test_resolve(test, user)
            list_test.append({
                'test': test.id,
                'title': test.title,
                'state': answered
            })
    
    if user.role == 'teacher':
        teaching = user.teaching_courses.first()
        if teaching: 
            teacher_tests =  teaching.tests.all()
            groups = teaching.teams.all()
        else:
            teacher_tests = None
            groups = None
    else:
        teacher_tests = None
        groups = None
        teaching = None

    if user.role == 'teacher':
        students = teaching.students.all()
    else:
        students = None

    context = {
        'tests': list_test,
        'role': user.role,
        'teacher_tests': teacher_tests,
        'groups': groups,
        'teaching': teaching,
        'notifications': user.notifications.all(),
        'students': students,
        'unread_notifications': user.notifications.filter(is_read=False).count(),
        'open_modal': request.GET.get('open_modal', 'false') == 'true',
    }

    return render(request, 'dashboard/test.html', context)

@login_required
def course(request):
    user = request.user
    course = user.course if user.role == 'student' else user.teaching_courses.first()
    
    if request.method == 'POST':
        if 'form-add-group' in request.POST:
            name = request.POST.get('name')
            Team.objects.create(name=name, course=course)
            messages.success(request, 'Se ha creado el grupo')
            return redirect('course')
        elif 'form-update-group' in request.POST:
            id_team = request.POST.get('task_id')
            team = get_object_or_404(Team, id=id_team)
            team.name = request.POST.get('name_update')
            team.save()
            messages.success(request, "El grupo se ha actualizado satisfactoriamente")
            return redirect('course')
        elif 'form-put-group' in request.POST:
            id_student = request.POST.get('user_id')
            print(id_student)
            student = get_object_or_404(CustomUser, id=id_student)
            team = request.POST.get('group')
            
            group = Team.objects.get(id=team)
            
            student.group = group
            student.save()
            messages.success(request, "Se ha agregado a un grupo")
            return redirect('course')

    if course:
        students = course.students.filter(is_active=True).all()
        teacher = course.teacher
        groups = course.teams.all()
    else:
        students = None
        teacher = None
        groups = None
    
    context = {
        'students': students,
        'role': request.user.role,
        'groups': groups,
        'teacher': teacher,
        'course': course,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
    }

    return render(request, 'dashboard/course.html', context)

@login_required
def profile(request):

    user = request.user
    form = CustomUserUpdateForm(instance=user)
    form_pass = CustomPasswordChangeForm(user=user)

    if request.method == 'POST':
        if 'form-update-user' in request.POST:
            form = CustomUserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Se ha actualizado")
                return redirect('profile')
        elif 'form-update-pass' in request.POST:
            form_pass = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, '¡Tu contraseña ha sido actualizada con éxito!')
                return redirect('profile')
        elif 'form-stress-share' in request.POST:
            share_stress_level = request.POST.get('share_stress_level') == 'on'
            user.share_stress_level = share_stress_level
            user.save()
            messages.success(request, "Se ha actualizado el estado de compartir tu nivel de estres")
            return redirect('profile')

    context = {
        'form': form,
        'form_pass': form_pass,
        'share_stress': user.share_stress_level,
        'role': user.role,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
    }

    return render(request, 'dashboard/profile.html', context)

@login_required
def test(request, test_id):
    user = request.user
    test = get_object_or_404(Test, id = test_id)
    questions = test.questions.all()

    if request.method == 'POST':
        tmp_stress = 0
        num_questions = questions.count()
        for question in questions:
            selected_option_value = request.POST.get(f'question_{question.id}')
            if selected_option_value:
                Answer.objects.create(
                    student=user,
                    question=question,
                    option=int(selected_option_value)
                )
                tmp_stress += int(selected_option_value)
        
        avg_stress = tmp_stress / num_questions
        stress_percentage = (avg_stress / 5) * 100

        user.stress = stress_percentage

        recommendation = Recommendation.objects.filter(
            min_percent__lte=stress_percentage - 5, 
            max_percent__gte=stress_percentage + 5
        ).first()

        user.recommendation = recommendation
        
        user.save()

        TestResult.objects.create(
            student=user,
            test=test,
            stress_percentage=stress_percentage
        )

        if request.user.stress > 50:
            teacher = test.course.teacher
            notify(request, [teacher], f'El estudiante {user.first_name} tiene un nivel elevado de estres', 'course')
        
        messages.success(request, 'El test se ha completado satisfactoriamente')    
        return redirect('list-test')
        
    context = {
        'role': request.user.role,
        'questions': questions,
        'test': test,
        'opts': Option.choices,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
    }

    return render(request, 'test/test_exe.html', context)

def create_task(title, due_date, course):

    if not due_date:
        return "Llena todos los campos", None

    task = Task.objects.create(
        title=title, 
        due_date=due_date, 
        course=course
    )

    return "La tarea se ha creado satisfactoriamente", task

@login_required
def delete_task(request, task_id):

    user = request.user
    course = user.teaching_courses.first()
    task = get_object_or_404(Task, id=task_id, course=course)

    task.delete()
    messages.success(request, 'La tarea se ha eliminado correctamente')
    return redirect('list-tasks')

@login_required
def delete_test(request, test_id):

    user = request.user
    test = get_object_or_404(Test, id=test_id)

    test.delete()
    messages.success(request, 'El test se ha eliminado correctamente')
    return redirect('list-test')


@login_required
def delete_team(request, team_id):

    user = request.user
    task = get_object_or_404(Team, id=team_id)
    task.delete()
    
    messages.success(request, 'El grupo se ha eliminado correctamente')
    return redirect('course')

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    
    if notification.is_read == False:
        notification.is_read = True
        notification.save()
    
    return redirect(notification.url)

@login_required
def notify(request, users, message, url):
    for user in users:
        Notification.objects.create(message=message, user=user, url=url)
    
@login_required
def recommendation(request):
    
    user = request.user
    
    form = RecommendationForm()
    
    if user.role == 'teacher':
        studens = user.teaching_courses.first().students.all() if user.teaching_courses.first() else None
    else:
        studens = None

    if request.method == 'POST':

        if 'form-update' in request.POST:
            recommendation = get_object_or_404(Recommendation, id=request.POST.get('recommendation'))

            recommendation.title = request.POST.get('title')
            recommendation.description = request.POST.get('description')
            recommendation.min_percent = request.POST.get('min_percent')
            recommendation.max_percent = request.POST.get('max_percent')

            recommendation.save()

            messages.success(request, 'La recomendación se actualizo correctamente')
            return redirect('recommendation')
        
        elif 'form-assign' in request.POST:
            student = get_object_or_404(CustomUser, id=request.POST.get('student'))
            recommendation = get_object_or_404(Recommendation, id=request.POST.get('recommendation'))
            
            student.recommendation = recommendation

            student.save()

            messages.success(request, 'La recomendación se asignó correctamente')

            return redirect('recommendation')
        else:
            form = RecommendationForm(request.POST)
            if form.is_valid():
                recommendation = form.save()
                messages.success(request, 'Se ha creado satisfactoriamente una recomendación')
                return redirect('recommendation')
    
    recommendations = Recommendation.objects.all()

    context = {
        'role': user.role,
        'recommendations': recommendations,
        'students': studens,
        'form': form,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
    }
    
    return render(request, 'dashboard/recommendation.html', context)

@login_required
def delete_recommendation(request, reco_id):
    recommendation = get_object_or_404(Recommendation, id = reco_id)
    recommendation.delete()
    messages.success(request, 'Se ha eliminado correctamente la recomendación')
    return redirect('recommendation')

@login_required
def user_admin(request):

    form = CustomUserCreationRoleForm()

    if request.method == 'POST':
        if 'form-create' in request.POST:
            form = CustomUserCreationRoleForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, 'El usuario se ha creado satisfactoriamente')
                return redirect('users')
        else:
            user = get_object_or_404(CustomUser, id=request.POST.get('user-id'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.dni = request.POST.get('dni')
            user.email = request.POST.get('email')

            user.save()
            
            messages.success(request, "Usuario actualizado satisfactoriamente")
            return redirect('users')

    user = request.user


    users = CustomUser.objects.all()


    context = {
        'role': user.role,
        'users': users,
        'form': form,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
    }

    return render(request, 'dashboard/user.html', context)

@login_required
def change_state_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    user.is_active = not user.is_active

    user.save()

    messages.success(request, f'El estado del usuario ({user.first_name} {user.last_name}) ha sido actualizado')

    return redirect('users')

@login_required
def course_admin(request):
    form = CreateCourseForm()

    if request.method == 'POST' and 'students' in request.POST:
        course_id = request.POST.get('course_id')
        student_ids = request.POST.getlist('students')
        course = Course.objects.get(id=course_id)

        for student_id in student_ids:
            student = CustomUser.objects.get(id=student_id, role='student')

            if student.course != course:  # i need check this
                student.group = None
            student.course = course
            student.save()

        messages.success(request, 'Estudiantes asignados correctamente al curso.')
        return redirect('courses')
    
    if request.method == 'POST':
        if 'course_id' in request.POST:
            course_id = request.POST.get('course_id')
            course = Course.objects.get(id=course_id)
            form = CreateCourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                messages.success(request, 'El curso se ha actualizado satisfactoriamente')
                return redirect('courses')
        else:
            form = CreateCourseForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'El curso se ha creado satisfactoriamente')
                return redirect('courses')

    user = request.user
    courses = Course.objects.all()
    teachers = CustomUser.objects.filter(role='teacher')
    students = CustomUser.objects.filter(role='student')

    print(students)

    context = {
        'role': user.role,
        'courses': courses,
        'form': form,
        'teachers': teachers,
        'students': students,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
    }

    return render(request, 'dashboard/course-admin.html', context)


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Se ha eleminado satisfactoriamente el curso')
    return redirect('courses')
    

@login_required
def desactivate_account_notification(request):
    user = request.user

    users = CustomUser.objects.filter(role='superuser')

    notify(request, users, f'El usuario {user.email} quiere desactivar su cuenta', 'users')

    messages.success(request, 'El administrador ha sido notificado y procesará tu solicitud pronto. Por favor, espera a que tu cuenta sea desactivada.')

    return redirect('profile')

from django.db.models import Avg, F

@login_required
def stats(request):

    user = request.user
    role = user.role

    if role == 'student':
        list_test_results = user.test_results.all()
        labels = [result.test.title for result in list_test_results]
        scores = [result.stress_percentage for result in list_test_results]
    else:
        labels = []
        scores = []
    
    if role == 'teacher':
        course = user.teaching_courses.first()

        aggregated_results = (
            TestResult.objects
            .filter(test__course=course)
            .values('test__title')
            .annotate(avg_stress=Avg('stress_percentage'))
        )

        labels_course = [entry['test__title'] for entry in aggregated_results]
        scores_course = [entry['avg_stress'] for entry in aggregated_results]

        teams_stats = {}

        for team in course.teams.all():
            team_students = team.members.all()

            aggregated_results = (
                TestResult.objects
                .filter(
                    student__in=team_students,
                    test__Team=team
                )
                .values('test__title')
                .annotate(avg_stress=Avg('stress_percentage'))
                .order_by('test__title') 
            )

            labelsg = []
            scoresg = []

            for entry in aggregated_results:
                labelsg.append(entry['test__title'])
                scoresg.append(entry['avg_stress'])

            teams_stats[team.name] = {
                'labelsg': labelsg,
                'scoresg': scoresg,
            }
        
        print(teams_stats)

    else:
        labels_course = []
        scores_course = []
        teams_stats = {}

    context = {
        'role': role,
        'labels': labels,
        'scores': scores,
        'labels_course': labels_course,
        'scores_course': scores_course,
        'teams_stats': teams_stats,
        'notifications': user.notifications.all(),
        'unread_notifications': user.notifications.filter(is_read=False).count(),
    }

    return render(request, 'dashboard/statistics.html', context)