from django.shortcuts import render
from django.http import HttpResponseServerError
from skating.db import DatabaseError, count_sessions

def home(request):
    try:
        return render(request, 'homepage/home.html', {'total': count_sessions()})
    except DatabaseError:
        return HttpResponseServerError('Не удалось получить данные. Попробуйте позже.')
