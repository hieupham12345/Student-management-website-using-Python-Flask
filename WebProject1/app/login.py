from flask import Flask, render_template, request, redirect, url_for, session,send_file
import mysql.connector
import hashlib
import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec
import matplotlib.backends.backend_pdf as pdf
import os
import io
from flask_mail import Mail
from flask_mail import Message
import random
import string
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4,A3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from PyPDF2 import PdfMerger,PdfReader
import base64
from email.mime.base import MIMEBase



mail_user=os.environ.get('outlook_mail_user')
mail_pass=os.environ.get('outlook_mail_pass')

app = Flask(__name__)
app.secret_key = os.environ.get('flask_secret_key')

@app.route('/')
def home():
	return render_template('login.html')

mail = Mail()
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = mail_user
app.config['MAIL_PASSWORD'] = mail_pass
mail.init_app(app)

class DatabaseConnector:
    def __init__(self, db_name):
        self.db_name = db_name
    def connect(self):
        if self.db_name == 'st':
            config = {
                'user': 'student',
                'password': 'password',
                'host': 'localhost',
                'database': 'studentmanagement'
            }
        elif self.db_name == 'lt':
            config = {
                'user': 'lecturer',
                'password': 'password',
                'host': 'localhost',
                'database': 'studentmanagement'
            }
        elif self.db_name=='ad':
            config = {
                'user': 'admin',
                'password': 'admin',
                'host': 'localhost',
                'database': 'studentmanagement'
            }
        elif self.db_name=='adminadmin':
            config={
                'user': 'adminadmin',
                'password': 'admin',
                'host': 'localhost',
                'database':'studentmanagement'}
        else:
            raise ValueError(f"Unsupported database name: {self.db_name}")
        
        try:
            conn = mysql.connector.connect(**config)
            return conn
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL database: {err}")
            return None

class Login:
    def __init__(self, username, password=''):
        self.username = username
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    def login(self):
        conn = DatabaseConnector(self.username[:2]).connect()
        cursor = conn.cursor()
        query = "select password from account where username=%s"
        cursor.execute(query, (self.username,))
        db_password = cursor.fetchone()[0]
        if db_password is not None and db_password == self.password :
            # Login successful
            self.attempts = 0
            return True
        else:
            return False

class PasswordChanger:   
    def __init__(self, username, old_password, new_password, confirm_password):
        self.username = username
        self.old_password = old_password
        self.new_password = new_password
        self.confirm_password = confirm_password  
    def change_password(self):
        cnx = DatabaseConnector('ad').connect()
        cursor = cnx.cursor()
        
        hashed_password = hashlib.sha256(self.old_password.encode('utf-8')).hexdigest()
        
        cursor.execute("select password from account where username=%s",(self.username,))
        password=''
        result=cursor.fetchone()
        if result is not None:
            password=result[0]
        else:
            password=''
        if hashed_password == password and self.new_password == self.confirm_password:
            query = "update account set password=sha2(%s,256) where username=%s"
            cursor.execute(query, (self.new_password, self.username))
            cnx.commit()
            cnx.close()
            return True     
        else: 
            return False

class Reset_password: ###
    def __init__(self,username='',email=''):
        self.username=username
        self.email=email
    def generate_password(self):
        password_characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(password_characters) for i in range(10))
        return password
    def change_pass(self):
        conn=DatabaseConnector('ad').connect()
        cursor=conn.cursor()
        if self.username[:2] == 'st':
            query = "SELECT email FROM student WHERE studentid=%s"
        elif self.username[:2] == 'lt':
            query = "SELECT email FROM lecturer WHERE lecturerid=%s"
        elif self.username[:2] == 'ad':
            query = "SELECT email FROM adminuser WHERE staffid=%s"
        cursor.execute(query, (self.username,))
        email_dtb = cursor.fetchone()           
        if email_dtb is not None and self.email.lower() == email_dtb[0].lower():
        #xu ly link reset password
            newpassword=self.generate_password()            
            msg = Message('Reset password', sender=mail_user, recipients=['tpmbdhieuvanpham@gmail.com']) ###user mail 
            msg.body = f'Your password has been changed. New password is {newpassword}, please login and change password immediately'
            mail.send(msg)
            cursor.execute("update account set password=sha2(%s,256) where username=%s",(newpassword,self.username,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            return False


# initialize dictionary to store failed login attempts
failed_login_attempts = {}
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(password) < 8:
            return render_template('login.html', error='Password must be at least 8 characters')  
        # check if user is locked out due to too many failed login attempts
        if username in failed_login_attempts and failed_login_attempts[username]['count'] >= 5:
            time_to_unlock = failed_login_attempts[username]['unlock_time']
            remaining_time = (time_to_unlock - datetime.datetime.now()).seconds
            return render_template('login.html', error='You have exceeded the maximum number of login attempts. Please try again later.', unlock_time=time_to_unlock, remaining_time=remaining_time)
        
        session['username']=username
        try:
            user = Login(username, password)
            if user.login()==True:
                if username[:2] == 'st':
                    failed_login_attempts.pop(username, None)
                    return render_template('home.html')
                elif username[:2] == 'lt':
                    failed_login_attempts.pop(username, None)
                    return render_template('lecturer_home.html')
                elif username[:4] == 'ad00':
                    failed_login_attempts.pop(username, None)
                    return render_template('ad_user_home.html')
                elif username=='adminadmin':
                    failed_login_attempts.pop(username, None)
                    return render_template('admin_home.html')                   
            elif user.login()==False:
                # Password incorrect
                if username in failed_login_attempts:
                    failed_login_attempts[username]['count'] += 1
                else:
                    failed_login_attempts[username] = {'count': 1}
                if failed_login_attempts[username]['count'] >= 5:
                    # lock out user for 5 minutes
                    time_to_unlock = datetime.datetime.now() + datetime.timedelta(minutes=5)
                    failed_login_attempts[username]['unlock_time'] = time_to_unlock
                    remaining_time = (time_to_unlock - datetime.datetime.now()).seconds
                    return render_template('login.html', error='You have exceeded the maximum number of login attempts. Please try again later.', unlock_time=time_to_unlock, remaining_time=remaining_time)
                else:
                    return render_template('login.html', error='Invalid username or password')
        except:
            # Error occurred while checking login credentials
            return render_template('login.html', error='An error occurred while checking your login credentials')
    else:
        # GET request, return login form
        return render_template('login.html')

#forget_pass
@app.route('/forgot_password')
def forgot_password():
	return render_template('forgot_password.html')
#reset_pass
@app.route('/reset_password', methods=["POST"])
def reset_password():
    username = request.form['username']
    email = request.form['email']
    a=Reset_password(username,email).change_pass()
    if a==True:
        return render_template('forgot_password.html',succeed="An email has been sent to reset your password. Please also check your spam folder ")
    return render_template('forgot_password.html', error='Wrong username or email')

#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#change_pass
@app.route('/change_password')
def change_password():
    tk=session['username']
    return render_template('change_password.html',tk=tk[:4])
@app.route('/change_password_result',methods=['POST'])
def change_password_result():
    if request.method=='POST':
        username = session['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if len(new_password) < 8:
            message = 'New password must be at least 8 characters'
            return render_template('change_password.html', message=message)
        elif new_password != confirm_password:
            message = 'New password and confirmation password do not match'
            return render_template('change_password.html', message=message)
        elif old_password == new_password:
            message = 'New password cannot be the same as old password'
            return render_template('change_password.html', message=message)
        else:       
            changer = PasswordChanger(username, old_password, new_password, confirm_password)
            if changer.change_password()==True:
                message = 'Change password successfully'
                return render_template('login.html', message_change_pass=message)
            else:
                message = "Wrong old password or new password and confirmation password are not the same"            
                return render_template('change_password.html', message=message)

class Schedule:
    def __init__(self, scheduleID='', courseID='', day='', time='', classroomID='', lecturerID='', semester=''):
        self.scheduleID = scheduleID
        self.courseID = courseID
        self.day = day
        self.time = time
        self.classroomID = classroomID
        self.lecturerID = lecturerID
        self.semester = semester
    def get_schedule(self,studentid): #tra ve schedule dang dict gom (coursename, day,time)
        conn=DatabaseConnector('st').connect()
        cursor=conn.cursor()
        if studentid:
            query="select coursename,day,time,classroomid,lecturer.name,status,student_schedule.scheduleid from student_schedule inner join schedule on student_schedule.scheduleid=schedule.scheduleid inner join course on schedule.courseid=course.courseid inner join lecturer on schedule.lecturerid=lecturer.lecturerid inner join attendance on schedule.scheduleid=attendance.scheduleid where studentid=%s order by day,time"
            cursor.execute(query,(studentid,))
            result=cursor.fetchall()
            schedule=[]
            for r in result:
                if r:
                    time=str(r[2])
                    sche={'Course Name': r[0],'Day': r[1],'Time':r[2],'Classroom ID':r[3],'Lecturer Name':r[4],'status':r[5],'Schedule ID':r[6]}
                    schedule.append(sche)
            cursor.close()
            conn.close()
            return schedule  

class Grade:
    def __init__(self, studentID='', courseID='', semester='', lecturerID='', process='',mid='',final='',avg='',credit=''):
        self.studentID = studentID
        self.courseID = courseID
        self.semester = semester
        self.lecturerID = lecturerID
        self.process = process
        self.mid=mid
        self.final=final
        self.avg=avg
        self.credit=credit
    def get_grade(self,studentid): #get grade + credit
        conn=DatabaseConnector('st').connect()
        cursor=conn.cursor()
        if studentid:
            query = "SELECT studentid,grade.courseid,semester,grade.lecturerid,process,mid,final,avg,credit FROM GRADE inner join course on grade.courseid=course.courseid	 WHERE STUDENTID= %s order by semester"
            cursor.execute(query, (studentid,))
            result = cursor.fetchall()
            list_gr=[]
            for r in result:
                gr=Grade(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
                list_gr.append(gr.__dict__)
        return list_gr
 
class Course:
    def __init__(self, courseID='', courseName='', facultyID='', credit='', description=None, previousCourse=None, followingCourse=None):
        self.courseID = courseID
        self.courseName = courseName
        self.facultyID = facultyID
        self.credit = credit
        self.description = description
        self.previousCourse = previousCourse
        self.followingCourse = followingCourse
    def get_course(self):
        conn=DatabaseConnector('st').connect()
        cursor=conn.cursor()
        query = "SELECT * FROM course"
        cursor.execute(query)
        result = cursor.fetchall()
        list_course=[]
        for r in result:
            c=Course(r[0],r[1],r[2],r[3],r[4],r[5],r[6])
            list_course.append(c)
        cursor.close()
        conn.close()
        return list_course
        
class Tuitionfee:
    def __init__(self,  tuitionFee='', status='', studentID='',sumcredit=''):
        self.tuitionFee = tuitionFee
        self.status = status
        self.studentID = studentID
        self.sumcredit=sumcredit
    def get_tuitionfee(self,studentid):
        conn=DatabaseConnector('st').connect()
        cursor=conn.cursor()
        if studentid:
            query = "SELECT * FROM TUITIONFEE WHERE STUDENTID=%s"
            cursor.execute(query,(studentid,))
            result=cursor.fetchone()
            if result:
                t=Tuitionfee(result[0], result[1], result[2], result[3])
                cursor.close()
                conn.close()
                return t

class TestSchedule:
    def __init__(self, scheduleID='',classroomID='', Time='', CourseID=''):
        self.scheduleID=scheduleID
        self.classroomID = classroomID
        self.Time = Time
        self.CourseID = CourseID
    def get_testschedule(self,studentid):  
        conn=DatabaseConnector('st').connect()
        cursor=conn.cursor()
        if studentid:
            query="select testschedule.courseid, coursename,testschedule.classroomid,testschedule.time from student_schedule inner join testschedule on student_schedule.scheduleid=testschedule.scheduleid inner join course on testschedule.courseid=course.courseid where studentid=%s"
            cursor.execute(query,(studentid,))
            result=cursor.fetchall()
            list_test=[]
            for r in result:
                test={'Course ID': r[0],'Course Name':r[1],'ClassroomID':r[2],'Time':r[3]}
                list_test.append(test)
            cursor.close()
            conn.close()
            return list_test


