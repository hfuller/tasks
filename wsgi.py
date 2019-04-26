from flask import Flask, render_template
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
    cursor.execute("select * from task where completed = FALSE order by priority, due asc")
    #return pprint.pformat(cursor.fetchall())
    return render_template('list.j2', tasks=cursor.fetchall())
