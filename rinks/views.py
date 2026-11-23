from django.shortcuts import render
from django.http import HttpResponseServerError
from skating.db import DatabaseError, rinks

def rink_list(request):
    try:
        return render(request, 'rinks/rink_list.html', {'rinks': rinks()})
    except DatabaseError:
        return HttpResponseServerError('Не удалось получить данные. Попробуйте позже.')
