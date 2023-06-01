from login import *
from ad_user import draw_pie_chart,setstyle_table
class Student:
    """
    class sinh viên chứa các phương thức cho sinh viên
    """
    db_conn=None
    def __init__(self, studentID='', name='', dateOfBirth='', gender='', address='', email='', phoneNumber='', classID=''):
        self.studentID = studentID
        self.name = name
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.address = address
        self.email = email
        self.phoneNumber = phoneNumber
        self.classID = classID
        if Student.db_conn is None:
            Student.db_conn=DatabaseConnector('st').connect()
    def update_info(self, email=None, phoneNumber=None, studentID=None,address=None):# update for student
        """
        phương thức cập nhập thông tin cá nhân:
        -Input: thông tin cần cập nhập (email, phone number, address, studentid)
        -Return: None
        """
        cursor = Student.db_conn.cursor()
        if email:
            cursor.execute("UPDATE Student SET email=%s WHERE studentID=%s", (email, studentID))
            self.email = email
        if phoneNumber:
            cursor.execute("UPDATE Student SET phoneNumber=%s WHERE studentID=%s", (phoneNumber, studentID))
            self.phoneNumber = phoneNumber
        if address:
            cursor.execute("Update student set address=%s where studentid=%s",(address,studentID))
            self.address=address
        Student.db_conn.commit()
    def get_info(self,studentid):
        """
        phương thức lấy thông tin cá nhân giảng viên
        -Input: studentID
        -Return: 1 dictionary chứa thông tin giảng viên
        """
        cursor = Student.db_conn.cursor()
        if studentid:
            query = "SELECT * FROM STUDENT WHERE STUDENTID= %s"
            cursor.execute(query, (studentid,))
            result = cursor.fetchone()
            if result is not None:
                student_info = Student(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                return student_info
    def register_course(self,studentid): #return list of register_course
        """
        phương thức lấy danh sách môn học sinh viên đã đăng kí học phần
        -Input: studentID
        -Return: 1 list dictionary chứa thông tin môn học
        """
        cursor=Student.db_conn.cursor()
        query="select course.courseid,coursename,credit from course_register inner join course on course_register.courseid=course.courseid where studentid=%s"
        cursor.execute(query,(studentid,))
        result=cursor.fetchall()
        list_register_courseid=[]
        for r in result:
            cs={'CourseID':r[0],'CourseName':r[1],'Credit':r[2]}
            list_register_courseid.append(cs)
        return list_register_courseid
    def save_course(self,studentid,courseid): #insert course to list register_course
        """
        phương thức đăng kí môn học (add vào list đăng kí)
        -Input: studentID, courseID
        -Return: True nếu add thành công vào database, false nếu thất bại
        """
        cursor=Student.db_conn.cursor()
        query = "INSERT INTO course_register (studentID, courseID) values(%s,%s)"
        cursor.execute(query,(studentid,courseid))
        Student.db_conn.commit()
    def del_course(self,studentid,courseid): #delete course in list register_course
        """
        phương thức xóa đăng kí môn học (del from list đăng kí)
        -Input: studentID, courseID
        -Return: True nếu delete thành công từ database, false nếu thất bại
        """
        cursor=Student.db_conn.cursor()
        query = "delete from course_register where studentid=%s and courseid=%s"
        cursor.execute(query,(studentid,courseid))
        Student.db_conn.commit()
    def st_attendance(self,studentid,scheduleid,time,note):
        """
        phương thức sinh viên điểm danh
        -Input: studentID, scheduleID, time, note
        -Return: true nếu insert database thành công, false nếu thất bại
        """
        cursor=Student.db_conn.cursor()
        query="insert into attendance_add (studentid,scheduleid,time,note) values (%s,%s,%s,%s)"
        cursor.execute(query,(studentid,scheduleid,time,note))
        Student.db_conn.commit()
        if cursor.rowcount>=1:
            return True
        return False
       
#profile
@app.route('/profile')
def profile():
    """
    hàm lấy thông tin profile user
    -Input: none
    -Return: page profile.html với thông tin user tương ứng
    """
    s=Student().get_info(session['username'])
    profile = s.__dict__
    return render_template('profile.html',profile=profile)

#dashboard
@app.route('/dashboard')
def dashboard():
    """
    hàm hướng tới dashboard
    -input: none
    -Return: page home.html
    """
    return render_template('home.html')

#schedule
@app.route('/schedule')
def schedule():
    """
    hàm hướng tới page thời khóa biểu
    Input: none
    return: page schedule.html với thông tin thời khóa biểu tương ứng
    """
    return render_template('schedule.html',schedule=Schedule().get_schedule(session['username']))

#courseRegister
@app.route('/courseregister')
def courseregister():
    """
    hàm hướng tới page đăng kí học phần
    -input: none
    -return: page course.html với thông tin danh sách môn học và danh sách đăng kí
    """
    username=session['username']
    l_re_courseid=Student().register_course(username)         
    course=Course().get_course()
    for c in course:
        c=c.__dict__
    return render_template('course.html',courses=course,course_register=l_re_courseid)

#grades
@app.route('/grades')
def grades():
    """
    hàm hướng tới page điểm số
    -Input: none
    -return: page grade.html với thông tin điểm số của user
    """
    grades = Grade().get_grade(session['username'])
    total_grade = 0
    sum_credit=0
    if len(grades)!=0:
        for grade in grades:
            if grade['avg'] is not None:
                total_grade += grade['avg']*grade['credit']
                sum_credit+=grade['credit']
            avg_grade = round(total_grade / sum_credit,2)
    else: 
        avg_grade=0
    return render_template('grade.html', grades=grades, avg_all=avg_grade)

#tuitionfee
@app.route('/tuitionfee')
def tuitionfee():
    """
    hàm hướng tới page học phí
    -Input: none
    -return: page grade.html với thông tin học phí của user
    """
    tuition=Tuitionfee().get_tuitionfee(session['username'])
    if tuition is not None:
        tuition=tuition.__dict__
    return render_template('tuitionfee.html',tuitionfee=tuition)

#testschedule
@app.route('/testschedule')
def testschedule():
    """
    hàm hướng tới page lịch thi
    -Input: none
    -return: page grade.html với thông tin lịch thi của user
    """
    test=TestSchedule().get_testschedule(session['username'])
    return render_template('testschedule.html',test=test)

#/save_course
@app.route('/save_course', methods=['POST'])
def save_course():
    """
    hàm save course, add course vào danh sách đăng kí học phần
    -Input: 1 list chứa các courseID
    -return: message thông báo thành công hay thất bại
    """
    course=Course().get_course()
    for c in course:
        c=c.__dict__
    if request.method == 'POST':
        if request.form.get('action') == 'save':
            selected = request.form.getlist('selected_course[]')
            for i in selected:
                try:
                    s=Student().save_course(session['username'],i)
                except Exception as e:
                    courseregister=Student().register_course(session['username'])
                    error=f"Fail: {str(e)}"
                    return render_template('course.html',message=error,course_register=courseregister,courses=course)
            courseregister=Student().register_course(session['username'])
            return render_template('course.html',courses=course,course_register=courseregister)
    return redirect(request.referrer)

#xoa_course
@app.route('/del_course', methods=['POST'])
def del_course():
    """
    hàm delete course, delete course từ danh sách đăng kí học phần
    -Input: 1 list chứa các courseID
    -return: message thông báo thành công hay thất bại
    """
    course=Course().get_course()
    for c in course:
        c=c.__dict__
    username=session['username']
    if request.method == 'POST':
        if request.form.get('action') == 'save':
            selected = request.form.getlist('selected_course[]')
            if selected:
                for i in selected:
                    s=Student().del_course(username,i)
                return redirect(url_for('courseregister'))
    return redirect(url_for('courseregister'))


#update_info
@app.route('/update_info', methods=['POST'])
def update_info():
    """
    hàm cập nhập thông tin
    -input: mail, phone, address
    -return: message thông báo thành công hay thất bại
    """
    mail = request.form['mail']
    phone = request.form['phone']
    address=request.form['address']
    try:
        Student().update_info(mail,phone,session['username'],address)
    except Exception as e:
        error_message = f"Error updating profile: {str(e)}"
        return render_template('profile.html', error_message=error_message,profile=Student().get_info(session['username']))
    return redirect('\profile')

@app.route('/st_attendance',methods=['POST'])
def st_attendance():
    """
    hàm tham gia điểm danh
    -input: username, time, note, scheduleid
    -return: message báo đã điểm danh thành công hay chưa
    """
    studentid=session['username']
    time=request.form['time']
    note=request.form['note']
    scheduleid=request.form['scheduleid']
    try:
        Student().st_attendance(studentid,scheduleid,time,note)
        mess='success'
    except Exception as e:
        mess=f"Fail. {str(e)}"
    return render_template('schedule.html',schedule=Schedule().get_schedule(session['username']),Message=mess)

def draw_bar_char_st(df):
    """
    hàm vẽ biểu đồ cột
    -input: dataframe chứa thông tin điểm số (cần có avg, và group by theo số lượng)
    -return: file pdf chứa biểu đồ
    """
    with pdf.PdfPages('bar_chart.pdf') as pdf_file:
        bins=[0,1,2,3,4,4.999,6,7,8,9,10]
        df['avg_bin']=pd.cut(df['avg'],bins=bins, include_lowest=True)
        count = df['avg_bin'].value_counts().sort_index()
        bar_chart = count.plot(kind='bar',color=['red', 'red', 'red', 'red','red', 'blue', 'blue','blue', 'blue','blue'],figsize=(8.27, 11.69)) 
        plt.title('Distribution of Average grade')
        plt.xlabel('Average Grades')
        plt.ylabel('Number of courses')
        plt.legend(['Number of courses'])
        plt.subplots_adjust(bottom=0.3)
        ax = plt.gca()
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        pdf_file.savefig()
        plt.clf()    
    return 'bar_chart.pdf'

@app.route('/st_download_report')
def st_download_report():
    """
    hàm download báo cáo file pdf
    -input: none
    -return: file báo cáo pdf tương ứng lựa chọn user
    """
    pdfmetrics.registerFont(TTFont('Tahoma', 'tahoma.ttf'))
    columns=('courseID', 'semester', 'lecturerID', 'process','mid','final','avg','credit')
    grades = Grade().get_grade(session['username'])
    df=pd.DataFrame(grades,columns=columns)
    total_grade=sum_credit=0
    if len(grades)!=0:
        for grade in grades:
            if grade['avg'] is not None:
                total_grade += grade['avg']*grade['credit']
                sum_credit+=grade['credit']
                avg_grade = round(total_grade / sum_credit,2)
            else: 
                avg_grade=0
    
    title=[['GRADE REPORT']]
    data=[columns]+[[col if col is not None else '' for col in row] for row in df.values]
    data.insert(0, ['GPA:', avg_grade])
  
    table=Table(title+data)
    table=setstyle_table(table)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate("table.pdf", pagesize=A4)
    doc.build([table])
    data = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    char_1=draw_bar_char_st(df)
    char_2=draw_pie_chart(df)
    pdf1=PdfReader(open(char_1,"rb"))
    pdf2=PdfReader(open(char_2,"rb"))
    pdf3 = PdfReader(open("table.pdf", "rb"))

    merger=PdfMerger()
    merger.append(pdf1)
    merger.append(pdf2)
    merger.append(pdf3)
    buffer=io.BytesIO()
    merger.write(buffer)
    buffer.seek(0)
    return send_file(buffer,download_name="grade report.pdf",as_attachment=False)
