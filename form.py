from flask import Flask,request,render_template,flash
import pymysql
app=Flask(__name__)

app.secret_key = b'\xc1\xb7\xd3\x19QV`\x0b\x19\x84\xf4;\\\xaaQ\xae\xf4A%\x1c\xf7H\xa5\x14'  # Replace with a secure, unique key


def get_db_connection():
    connection=pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='emp',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        user=request.form
        name=user['name']
        city=user['city']
        
        connection = get_db_connection()

        with connection.cursor() as cursor:
            # Prepare SQL query to insert a record into the database.
            sql = "INSERT INTO empdetail (name, city) VALUES (%s, %s)"
            cursor.execute(sql, (name, city))

        # Commit changes in the database
        connection.commit()
        connection.close()
    return render_template("form.html")

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method=="POST":
        user=request.form
        name=user["name"]
        name2=user["name2"]
        
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            sql = "UPDATE empdetail SET name = %s WHERE name = %s "

            cursor.execute(sql,(name2,name))
            
        
        connection.commit()
        flash("Update Successful")
        connection.close()
    return render_template("form.html")

@app.route('/show',methods=['GET','POST'])
def show():
    ad=None
    name=request.args.get('name')

        
    if name:  # Only query if 'name' is provided
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Fetch rows from empdetail table where name matches
                sql = "SELECT name, city FROM empdetail WHERE name = %s"
                cursor.execute(sql, (name,))
                ad = cursor.fetchall()  # Fetch all matching rows as tuples
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            connection.close()
    return render_template("form.html",ad=ad)

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=="POST":
        name=request.form['name']
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "DELETE FROM empdetail  WHERE name = %s "

            cursor.execute(sql,(name,))
        connection.commit()
        connection.close()
    return render_template("form.html")
    
    
if __name__ == '__main__':
    app.run(debug=True)