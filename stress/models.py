from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Ingrese un correo válido')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')

        return self.create_user(email, password, **extra_fields)

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='teaching_courses', limit_choices_to={'role': 'teacher'})
    def __str__(self):
        return f"{self.name} -> {self.teacher}"

class Team(models.Model):
    name = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return f"{self.name}"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Alumno'),
        ('teacher', 'Profesor'),
        ('superuser', 'Administrador'),
    ]

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    dni = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    stress = models.IntegerField(default=0)
    share_stress_level = models.BooleanField(default=False)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    group = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"{self.title}"

class Test(models.Model):
    title = models.CharField(max_length=255)
    Team = models.ManyToManyField(Team, related_name='tests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests', default='2')

    def __str__(self):
        return f"{self.title}"

class Question(models.Model):
    description = models.CharField(max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f"{self.description}"

class Option(models.IntegerChoices):
    NUNCA = 1, 'Nunca'
    RARA_VEZ = 2, 'Rara vez'
    A_VECES = 3, 'A veces'
    CASI_SIEMPRE = 4, 'Casi siempre'
    SIEMPRE = 5, 'Siempre'

class Answer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers', limit_choices_to={'role': 'student'})
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.IntegerField(choices=Option.choices)

    def __str__(self):
        return f"{self.student} = {self.question} -> {self.option}"

