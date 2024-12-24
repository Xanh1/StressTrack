from .models import Answer

def test_resolve(test, user):    
    answered = Answer.objects.filter(student=user,question__test=test).exists()
    return answered