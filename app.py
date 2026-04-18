from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reservations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  date TEXT NOT NULL,
                  guests INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        date = f"{year}-{month}-{day}"
        guests = request.form['guests']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO reservations (name, phone, date, guests) VALUES (?, ?, ?, ?)",
                  (name, phone, date, guests))
        conn.commit()
        conn.close()
        return redirect(url_for('success', name=name, date=date, guests=guests))
    return render_template('reservation.html')

@app.route('/success')
def success():
    name = request.args.get('name')
    date = request.args.get('date')
    guests = request.args.get('guests')
    return render_template('success.html', name=name, date=date, guests=guests)

@app.route('/my_reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = []
    phone = request.args.get('phone', '')
    searched = False
    deleted = request.args.get('deleted', False)

    if request.method == 'POST':
        phone = request.form['phone']
        searched = True
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM reservations WHERE phone=? ORDER BY id DESC", (phone,))
        reservations = c.fetchall()
        conn.close()
    elif phone:
        searched = True
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM reservations WHERE phone=? ORDER BY id DESC", (phone,))
        reservations = c.fetchall()
        conn.close()

    return render_template('my_reservations.html',
                           reservations=reservations,
                           phone=phone,
                           searched=searched,
                           deleted=deleted)

@app.route('/delete_reservation/<int:id>')
def delete_reservation(id):
    phone = request.args.get('phone', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM reservations WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('my_reservations') + '?deleted=1&phone=' + phone)

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reservations ORDER BY id DESC")
    reservations = c.fetchall()
    conn.close()
    return render_template('admin.html', reservations=reservations)

@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM reservations WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')