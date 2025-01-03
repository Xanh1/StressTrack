from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm, CustomPasswordChangeForm
from .models import Test, Option, Answer, Task, Team, CustomUser, Question
from django.contrib.auth.decorators import login_required
from .utils import test_resolve
from datetime import date

def home(request):
    if request.user.is_authenticated:
        return redirect('panel')
    return render(request, 'index.html')

def log_in(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('panel')
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

    if course:
        tasks = course.tasks.filter(due_date__gte=date.today()).order_by('due_date')

    if team:
        tests = team.tests.all()

    stress = user.stress
    color = ""

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
        'stress': stress,
        'role': user.role,
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
            response = create_task(title, due_date, course)
            messages.success(request, response)
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
    }

    return render(request, 'dashboard/task.html', context)

@login_required
def list_tests(request):

    user = request.user

    team = user.group

    if request.method == 'POST':
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
        tests = team.tests.all()
    else:
        tests = None
    
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
        teacher_tests =  user.teaching_courses.first().tests.all()
    else:
        teacher_tests = None

    context = {
        'tests': list_test,
        'role': user.role,
        'teacher_tests': teacher_tests,
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
        students = course.students.all()
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
    }

    return render(request, 'dashboard/profile.html', context)

@login_required
def test(request, test_id):        
    test = get_object_or_404(Test, id = test_id)
    questions = test.questions.all()

    if request.method == 'POST':
        tmp_stress = 0
        for question in questions:
            selected_option_value = request.POST.get(f'question_{question.id}')
            if selected_option_value:
                Answer.objects.create(
                    student=request.user,
                    question=question,
                    option=int(selected_option_value)
                )
                tmp_stress += int(selected_option_value)
        
        request.user.stress = tmp_stress
        request.user.save()
        messages.success(request, 'El test se ha completado satisfactoriamente')    
        return redirect('list-test')
        
    context = {
        'role': request.user.role,
        'questions': questions,
        'test': test,
        'opts': Option.choices
    }

    return render(request, 'test/test_exe.html', context)

def create_task(title, due_date, course):

    if not due_date:
        return "Llena todos los campos"

    task = Task.objects.create(
        title=title, 
        due_date=due_date, 
        course=course
    )

    return "La tarea se ha creado satisfactoriamente"

@login_required
def delete_task(request, task_id):

    user = request.user
    course = user.teaching_courses.first()
    task = get_object_or_404(Task, id=task_id, course=course)

    task.delete()
    messages.success(request, 'La tarea se ha eliminado correctamente')
    return redirect('list-tasks')

@login_required
def delete_team(request, team_id):

    user = request.user
    task = get_object_or_404(Team, id=team_id)
    task.delete()
    
    messages.success(request, 'El grupo se ha eliminado correctamente')
    return redirect('course')