from flask import Flask, json, render_template, request, redirect, url_for, flash,  jsonify
from flask_mysqldb import MySQL


# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'baf8d5ac3debb5'
app.config['MYSQL_PASSWORD'] = '5b136e8f'
app.config['MYSQL_DB'] = 'heroku_97268bb8b0abec4'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    data = cur.fetchall()
    cur.close()
    print(data)
    return jsonify(data)

@app.route('/register', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        usuario = {
            "nombre": request.json["nombre"],
            "apellidoP": request.json["apellidoP"],
            "apellidoM": request.json["apellidoM"],
            "dni": request.json["dni"],
            "contrasena": request.json["contrasena"],
            "tipoUsuario": request.json["tipoUsuario"],
            "correo": request.json["correo"]
        }

        cur1 = mysql.connection.cursor()
        cur1.execute('CALL heroku_97268bb8b0abec4.registrarpaciente2(%s,%s,%s,%s,%s,%s, %s);', (usuario["nombre"], usuario["apellidoP"], usuario["apellidoM"], usuario["dni"], usuario["contrasena"], usuario["tipoUsuario"], usuario["correo"]))
        # data = cur.fetchall()
        # cur1.close()
        mysql.connection.commit()

        cur2 = mysql.connection.cursor()
        cur2.execute('SELECT * FROM user Where dni=%s', [usuario['dni']])
        data = cur2.fetchall()
        cur2.close()
        print(data)
        return jsonify(data)


@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3003, debug=True)
