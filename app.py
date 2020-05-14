#todo-application
from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="todo_list"
)

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    # Fetch all data form database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM todo_table")
    data = list(mycursor)
    #----------------------------
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `todo_table` WHERE status='projects'")
    projects_data = list(mycursor)
    

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `todo_table` WHERE status='tasks'")
    tasks_data = list(mycursor)
    

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `todo_table` WHERE status='commitments'")
    commitments_data = list(mycursor)
    
    

    return render_template('index.html',data = data,projects_data = projects_data,commitments_data=commitments_data,tasks_data=tasks_data)


@app.route('/add',methods = ['POST','GET'])
def add():
    
    title=request.form.get('title')  
    desc=request.form.get('desc')
    catagory = request.form.get('radio')
    if catagory == None:
        catagory = "projects"
#   insert data in database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT MAX(ID) FROM todo_table")
    max_id = list(mycursor)[0][0]
    sql = "INSERT INTO todo_table (id, title,disc,date,status) VALUES (%s, %s,%s, %s,%s)"
    val = (max_id+1, title,desc,datetime.datetime.now(),catagory)
    mycursor.execute(sql, val)
    mydb.commit()
#   ------------------------------------
    
    
    return redirect(url_for("home"))

@app.route('/delete',methods = ['POST','GET'])
def delete():
    selected=request.form.getlist("checkbox")
    # Delete items database using list
    for id in selected:
        mycursor = mydb.cursor()
        sql = "DELETE FROM `todo_table` WHERE ID= %s"
        adr = (id, )
        mycursor.execute(sql, adr)
        mydb.commit()
    #--------------------------------
    
    return redirect(url_for("home"))


app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(debug=True)
