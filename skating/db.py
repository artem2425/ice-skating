import sqlite3
from pathlib import Path
from django.conf import settings

class DatabaseError(Exception):
    pass

def query(sql, params=(), one=False):
    connection = None
    try:
        connection = sqlite3.connect(str(Path(settings.BASE_DIR) / 'data' / 'skating.db'))
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(sql, params)
        rows = cursor.fetchone() if one else cursor.fetchall()
        return dict(rows) if one and rows else None if one else [dict(row) for row in rows]
    except sqlite3.Error as exc:
        raise DatabaseError('Не удалось получить данные. Попробуйте позже.') from exc
    finally:
        if connection is not None:
            connection.close()

SESSION_SELECT = '''SELECT s.id, s.title, s.slug, s.session_kind, s.start_date, s.duration, s.skaters, s.status, s.rink_id, r.name AS rink_name, r.capacity AS rink_capacity, r.rink_kind FROM skating s LEFT JOIN rinks r ON s.rink_id = r.id'''

def sessions(min_skaters=None, sort='date_asc', limit=None):
    sorts = {'date_asc': 's.start_date ASC', 'date_desc': 's.start_date DESC', 'skaters_asc': 's.skaters ASC', 'skaters_desc': 's.skaters DESC'}
    sql = SESSION_SELECT
    params = []
    if min_skaters is not None:
        sql += ' WHERE s.skaters >= ?'
        params.append(min_skaters)
    sql += ' ORDER BY ' + sorts.get(sort, sorts['date_asc']) + ', s.id ASC'
    if limit is not None:
        sql += ' LIMIT ?'
        params.append(limit)
    return query(sql, params)

def session(slug):
    return query(SESSION_SELECT + ' WHERE s.slug = ?', (slug,), one=True)

def rinks():
    return query('SELECT id, name, capacity, rink_kind FROM rinks ORDER BY id')

def count_sessions():
    return query('SELECT COUNT(*) AS total FROM skating', one=True)['total']

def statistics():
    return query('SELECT session_kind, COUNT(*) AS total FROM skating GROUP BY session_kind HAVING COUNT(*) >= ? ORDER BY total DESC, session_kind', (2,))
