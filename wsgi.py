from flask import Flask, render_template, redirect, request, abort
import psycopg2, psycopg2.extras
import pprint

app = Flask(__name__)

print("Opening DB")
conn = psycopg2.connect(dbname="tasks", cursor_factory=psycopg2.extras.RealDictCursor)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
print(conn)

@app.route('/')
def list_tasks_html():
    cursor = conn.cursor()
    cursor.execute("select * from task where completed = FALSE order by due asc, priority desc")
    #return pprint.pformat(cursor.fetchall())
    return render_template('list.j2', tasks=cursor.fetchall())

@app.route('/task', methods=['POST'])
def add_task():
    priority = int(request.form.get('priority', default="0"))
    summary = request.form.get('summary')
    due = request.form.get('due')
    print(priority, summary, due)

    cursor = conn.cursor()
    cursor.execute("insert into task (priority, summary, due) values (%(priority)s, %(summary)s, %(due)s)", {
        'priority': priority,
        'summary': summary,
        'due': due
    })
    return redirect('/')

@app.route('/task/<id>', methods=['DELETE', 'GET'])
def delete_task(id):
    if request.method != 'DELETE' and request.args['_method'] != 'DELETE':
        return abort(400)
    id = int(id)
    cursor = conn.cursor()
    cursor.execute('delete from task where id = %s', (id,))
    return redirect('/')


