import sqlite3

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('tasks.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
def add_task(user_id, task):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (user_id, task) VALUES (?, ?)', (user_id, task))
    conn.commit()
    conn.close()

def get_tasks(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, task FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
def mark_task_completed(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET task = task || " ☑" WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

