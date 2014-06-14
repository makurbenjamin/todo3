import sqlite3
from bottle import route, run, debug, template, request, static_file, error

@route('/')
@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1';")
    result = c.fetchall()
    c.close()
    output = template('make_table', rows=result)
    return output

@route('/new', method='GET')
def new_item():
    if request.GET.get('save','').strip():
        new = request.GET.get('task', '').strip()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
        new_id = c.lastrowid
        conn.commit() 
        c.close() 
        return '<p>The new task was inserted into the database, the ID is %s</p><p><a href="/">Show all tasks...</a></p>' % new_id 
    else:
        return template('new_task.tpl')

@route('/edit/:no', method='GET')
def edit_item(no):
    if request.GET.get('save','').strip():
        edit = request.GET.get('task','').strip()
        status = request.GET.get('status','').strip()
        if status == 'open':
            status = 1
        else:
            status = 0
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit,status,no))
        conn.commit()
        return '<p>The item number %s was successfully updated</p><p><a href="/">Show all tasks...</a></p>' %no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
        cur_data = c.fetchone()
        return template('edit_task', old = cur_data, no = no)

@route('/item:item#[0-9]+#')
def show_item(item):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
        result = c.fetchone()
        c.close()
        if not result:
            return '<p>This item number does not exist!</p><p><a href="/">Show all tasks...</a></p>'
        else:
            return 'Task: %s <p><a href="/">Show all tasks...</a></p>' %result[0]

@route('/help')
def help():
    return static_file('help.html', root='.')

@route('/css/:filename', name='css')
def server_static(filename):
    return static_file(filename, root='./css')

@error(403)
def mistake403(code):
    return '<p>There is a mistake in your url!</p>'

@error(404)
def mistake404(code):
    return '<p>Sorry, this page does not exist!</p>'

debug(True)
run(reloader=True)
#remember to remove reloader=True and debug(True) when you move your application from development to a productive environment