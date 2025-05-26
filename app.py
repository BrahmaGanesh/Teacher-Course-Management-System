from flask import Flask, render_template,request,redirect,flash,session
from db_config import get_connection
from functools import wraps

app = Flask(__name__)
app.secret_key="ganesh123"

@app.route("/",methods=["POST","GET"])
def login():
   if request.method == "POST":
       username=request.form["username"]
       password=request.form["password"]
       conn=get_connection()
       cursor=conn.cursor(dictionary=True)
       cursor.execute("SELECT * FROM admin_users WHERE username=%s",(username,))
       user=cursor.fetchone()
       conn.close()
       if user and user['password'] == password:
           session["admin_logged"]=True
           session["admin_username"]=user["username"]
           return redirect("/dashboard")
       else:
           flash("Invalid user","danger")
           redirect("/")
   return render_template("login.html")


@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        username=request.form["username"]
        password= request.form["password"]
        conn=get_connection()
        cursor=conn.cursor(dictionary=True)
        query="INSERT INTO admin_users(username,password) VALUES(%s,%s)"
        cursor.execute(query,(username,password))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("register.html")
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged"):
            flash("Login required", "warning")
            return redirect("/")  # redirect to login page
        return f(*args, **kwargs)
    return decorated_function
@app.route("/dashboard")
def dashboard():
    if session:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total_teachers FROM teachers")
        teachers = cursor.fetchone()["total_teachers"]

        cursor.execute("SELECT COUNT(*) AS total_courses FROM courses")
        courses = cursor.fetchone()["total_courses"]

        cursor.execute("SELECT COUNT(*) AS unassigned FROM courses WHERE teacher_id IS NULL")
        unassigned = cursor.fetchone()["unassigned"]

        cursor.execute("SELECT ROUND(AVG(experience),1) AS avg_exp FROM teachers")
        avg_exp = round(cursor.fetchone()["avg_exp"])

        conn.close()
    
        return render_template("index.html", teachers=teachers, courses=courses, unassigned=unassigned, avg_exp=avg_exp)
    else:
        flash("Login first","danger")
        return redirect("/")

@app.route('/teachers')
@login_required
def teacher():
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM teachers")
    teachers= cursor.fetchall()
    conn.close()
    return render_template("teachers.html",teachers=teachers)

@app.route('/add_teacher',methods=["GET","POST"])
def add_teacher():
    if request.method == "POST":
        name=request.form["name"]
        experience=request.form["experience"]

        query="  INSERT INTO teachers(name,experience) VALUES (%s,%s)"
        conn = get_connection()
        cursor=conn.cursor()
        cursor.execute(query,(name,experience))
        conn.commit()
        conn.close()
        return redirect('/teachers')
    return render_template("add_teachers.html")

@app.route('/courses')
@login_required
def courses():
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    query="SELECT c.course_id,c.course_name,t.name FROM courses AS c LEFT JOIN teachers AS t ON c.teacher_id=t.id"
    cursor.execute(query)
    courses=cursor.fetchall()
    return render_template('courses.html',courses=courses)

@app.route("/add_courses",methods=["POST","GET"])
@login_required
def add_courses():
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM TEACHERS")
    teachers=cursor.fetchall()
    if request.method == "POST":
        course_name=request.form["name"]
        teacher_id=request.form["teacher_id"]
        teacher_id=teacher_id if teacher_id else None
        cursor.execute("INSERT INTO courses(course_name,teacher_id) VALUES (%s,%s)", (course_name,teacher_id))
        conn.commit()
        conn.close()
        return redirect('/courses')
    conn.close()
    return render_template("add_courses.html",teachers=teachers)

@app.route('/edit_teacher/<int:teacher_id>',methods=["POST","GET"])
@login_required
def edit_teacher(teacher_id):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)

    if request.method == "POST":
        name=request.form['name']
        experience=request.form["experience"]
        query="UPDATE TEACHERS SET name=%s,experience=%s WHERE id=%s"
        cursor.execute(query,(name,experience,teacher_id))
        conn.commit()
        conn.close()
        flash(teacher_id,"success")
        return redirect('/teacher')
    cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
    teacher = cursor.fetchone()
    conn.close()
    return render_template("add_teachers.html",teacher=teacher)
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
