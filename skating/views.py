from datetime import datetime
from django.http import Http404, HttpResponseServerError
from django.shortcuts import render
from .db import DatabaseError, sessions, session, statistics as get_statistics

def prepare_date(record):
    record['start_date'] = datetime.fromisoformat(record['start_date'])
    return record

def skate_list(request):
    raw = request.GET.get('skaters', '').strip()
    try:
        minimum = max(0, int(raw)) if raw else None
    except ValueError:
        minimum = None
    sort = request.GET.get('sort', 'date_asc')
    if sort not in ('date_asc', 'date_desc', 'skaters_asc', 'skaters_desc'):
        sort = 'date_asc'
    raw_limit = request.GET.get('limit', '')
    limit = int(raw_limit) if raw_limit in ('3', '5', '10') else None
    try:
        items = [prepare_date(item) for item in sessions(minimum, sort, limit)]
        return render(request, 'skating/skate_list.html', {'sessions': items, 'skaters': raw, 'sort': sort, 'limit': str(limit or '')})
    except DatabaseError:
        return HttpResponseServerError('Не удалось получить данные. Попробуйте позже.')

def skate_detail(request, slug):
    try:
        item = session(slug)
        if item is None:
            raise Http404('Сеанс не найден')
        return render(request, 'skating/skate_detail.html', {'session': prepare_date(item)})
    except DatabaseError:
        return HttpResponseServerError('Не удалось получить данные. Попробуйте позже.')

def statistics(request):
    try:
        return render(request, 'skating/statistics.html', {'statistics': get_statistics()})
    except DatabaseError:
        return HttpResponseServerError('Не удалось получить данные. Попробуйте позже.')
