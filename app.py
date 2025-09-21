from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
      password="pass123",
  # your MySQL password
        database="hospital"
    )

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rahul (BasicWards, ID, pName, Gender, Age, birth, Injury, Blood, Medicalhistory,
                           Treatment, Email, room, admit, symptoms, advance, num, religion, Address)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (data['BasicWards'], data['ID'], data['pName'], data['Gender'], data['Age'], data['birth'],
          data['Injury'], data['Blood'], data['Medicalhistory'], data['Treatment'], data['Email'],
          data['room'], data['admit'], data['symptoms'], data['advance'], data['num'], data['religion'], data['Address']))
    conn.commit()
    conn.close()
    return redirect('/view')

@app.route('/view')
def view():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rahul")
    rows = cursor.fetchall()
    conn.close()
    return render_template('view.html', patients=rows)

@app.route('/delete/<id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rahul WHERE ID=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/view')

@app.route('/edit/<id>')
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rahul WHERE ID=%s", (id,))
    row = cursor.fetchone()
    conn.close()
    return render_template('edit.html', patient=row)

@app.route('/update/<id>', methods=['POST'])
def update(id):
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE rahul SET BasicWards=%s, pName=%s, Gender=%s, Age=%s, birth=%s,
        Injury=%s, Blood=%s, Medicalhistory=%s, Treatment=%s, Email=%s,
        room=%s, admit=%s, symptoms=%s, advance=%s, num=%s, religion=%s, Address=%s
        WHERE ID=%s
    """, (data['BasicWards'], data['pName'], data['Gender'], data['Age'], data['birth'],
          data['Injury'], data['Blood'], data['Medicalhistory'], data['Treatment'],
          data['Email'], data['room'], data['admit'], data['symptoms'], data['advance'],
          data['num'], data['religion'], data['Address'], id))
    conn.commit()
    conn.close()
    return redirect('/view')

@app.route('/clear')
def clear():
    return redirect('/')

@app.route('/exit')
def exit():
    return "Application Closed (Logout)"

if __name__ == "__main__":
    app.run(debug=True)
