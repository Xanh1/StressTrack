from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Test, Option, Answer
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

    course = user.course

    if course:
        tasks = course.tasks.all()
    else:
        tasks = None
    
    context = {
        'tasks': tasks,
        'role': user.role,
    }

    return render(request, 'dashboard/task.html', context)

@login_required
def list_tests(request):

    user = request.user

    team = user.group

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

    context = {
        'tests': list_test,
        'role': user.role,
    }

    return render(request, 'dashboard/test.html', context)

@login_required
def course(request):

    course = request.user.course.students.all()

    context = {
        'course': course,
        'role': request.user.role
    }

    return render(request, 'dashboard/course.html', context)

# I need change this and create a new form, couse I need to add an attribute to share the stress level.
@login_required
def profile(request):

    user = request.user
    form = CustomUserCreationForm(instance=user)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('panel')

    context = {
        'form': form,
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

@login_required
def create_task(request):

    user = request.user

    if user.teaching_courses.count() == 0:
        messages.error(request,"No esta asignado a un curso por el momento")
        return redirect('list-tasks')

    return render(request, 'index.html')