from login import *
class Lecturer:
    db_conn=None
    def __init__(self, lecturerID='', name='', dateOfBirth='', gender='', address='', email='', phoneNumber='', facultyID=''):
        self.lecturerID = lecturerID
        self.name = name
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.address = address
        self.email = email
        self.phoneNumber = phoneNumber
        self.facultyID = facultyID
        Lecturer.db_conn=DatabaseConnector('lt').connect()
    def update_info(self, name=None, email=None, phoneNumber=None, lecturerID=None,address=None):# update for
        cursor=Lecturer.db_conn.cursor()
        if name:
            cursor.execute("UPDATE lecturer SET name=%s WHERE lecturerid=%s", (name, lecturerID))
            self.name = name
        if email:
            cursor.execute("UPDATE lecturer SET email=%s WHERE lecturerid=%s", (email, lecturerID))
            self.email = email
        if phoneNumber:
            cursor.execute("UPDATE lecturer SET phoneNumber=%s WHERE lecturerid=%s", (phoneNumber, lecturerID))
            self.phoneNumber = phoneNumber
        if address:
            cursor.execute("Update lecturer set address=%s where lecturerid=%s",(address,lecturerID))
            self.address=address
        Lecturer.db_conn.commit()
    def get_info(self,lecturerID):
        cursor = Lecturer.db_conn.cursor()
        if lecturerID:
            query = "SELECT * FROM lecturer WHERE lecturerID= %s"
            cursor.execute(query, (lecturerID,))
            result = cursor.fetchone()
            if result is not None:
                lecturer_info = Lecturer(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                return lecturer_info
    def get_list_class(self,lecturerID): #get list class của học kì này (trong schedule)
        cursor=Lecturer.db_conn.cursor()
        cursor.execute("select distinct day,time,classroomid,course.courseid,coursename,semester,schedule.scheduleid,status from schedule inner join course on schedule.courseid=course.courseid  inner join attendance on schedule.scheduleid=attendance.scheduleid where schedule.lecturerid=%s",(lecturerID,))
        result=cursor.fetchall()
        l_class=[]
        if result:
            for r in result:
                time=str(r[1])
                c={'Day':r[0],'Time':time,'classroom ID':r[2],'Course ID':r[3],'Course Name':r[4],'Semester':r[5],'Schedule ID':r[6],'status':r[7]}
                l_class.append(c)
        return l_class
    def get_list_class_previous(self,lecturerID): #list_class học  kì trước
        cursor=Lecturer.db_conn.cursor()
        cursor.execute("select distinct grade.courseid,coursename,semester from grade inner join course on grade.courseid=course.courseid where grade.lecturerid=%s",(lecturerID,))
        result=cursor.fetchall()
        l_class_pre=[]
        if result:
            for r in result:
                c={'Course ID':r[0],'Course Name':r[1],'Semester':r[2]}
                l_class_pre.append(c)
        return l_class_pre
    def get_list_student_class_previous(self,courseID,semester,lecturerID): #get list student học kì trước (from grade)
        query = "SELECT student.studentID, name, process,mid,final,avg FROM grade INNER JOIN student ON grade.studentid = student.studentid WHERE courseid = %s AND semester = %s AND lecturerid = %s;"
        cursor=Lecturer.db_conn.cursor()
        cursor.execute(query,(courseID,semester,lecturerID))
        results = cursor.fetchall()
        return results
    def get_list_student_class(self,scheduleid): #get list student học kì này (from schedule)
        cursor=Lecturer.db_conn.cursor()
        cursor.execute("select student.studentid,name from student inner join student_schedule on student.studentid=student_schedule.studentid where scheduleid=%s",(scheduleid,))
        result=cursor.fetchall()
        st_list=[]
        for r in result:
            st={'Student ID':r[0],'Name':r[1]}
            st_list.append(st)
        return st_list
    def get_list_student_class_grade(self,semester,courseid,lecturerid):
        cursor=Lecturer.db_conn.cursor()
        query="select studentid,process,mid,final from grade where semester=%s and courseid=%s and lecturerid=%s"
        cursor.execute(query,(semester,courseid,lecturerid))
        result=cursor.fetchall()
        l_grade_st=[]
        for r in result:
            gr={'Student ID':r[0],'process':r[1],'mid':r[2],'final':r[3]}
            l_grade_st.append(gr)
        return l_grade_st
    def update_attendance(self,scheduleid,status):
        cursor=Lecturer.db_conn.cursor()
        if status=='open':
            query="update attendance set status='close' where scheduleid=%s"
        else:
            query="update attendance set status='open' where scheduleid=%s"
        cursor.execute(query,(scheduleid,))
        Lecturer.db_conn.commit()
        if cursor.rowcount>=1:
            return True
        return False
    def get_list_attendance_st(self,lecturerid='',scheduleid=''):
        cursor=Lecturer.db_conn.cursor()
        if scheduleid!='':
            query="select student.studentid,name,note,attendance_add.scheduleid from attendance_add inner join student on attendance_add.studentid=student.studentid where scheduleid=%s"
            cursor.execute(query,(scheduleid,))
        else:       
            query="select student.studentid,name,note,attendance_add.scheduleid from attendance_add inner join student on attendance_add.studentid=student.studentid inner join schedule on attendance_add.scheduleid=schedule.scheduleid where lecturerid=%s"
            cursor.execute(query,(lecturerid,))
        result=cursor.fetchall()
        l_st_att=[]
        for r in result:
            st={'Student ID':r[0],'Student Name':r[1],'Note':r[2],'Schedule ID':r[3]}
            l_st_att.append(st)
        return l_st_att
    def delete_att_after_download(self,scheduleid):
        cursor=Lecturer.db_conn.cursor()
        query="delete from attendance_add where scheduleid=%s"
        cursor.execute(query,(scheduleid,))
        if cursor.rowcount>=1:
            Lecturer.db_conn.commit()
            return True
        return False

#lecturer_home
@app.route('/lecturer_home')
def lecturer_home():
    return render_template('lecturer_home.html')

#lecturer_profile
@app.route('/lecturer_profile')
def lecturer_profile():
    l=Lecturer().get_info(session['username'])
    l = l.__dict__
    return render_template('lecturer_profile.html',profile=l)

#update info
@app.route('/lecturer_update_info',methods=['POST'])
def lecturer_update_info():
    name = request.form['name']
    mail = request.form['mail']
    phone = request.form['phone']
    address=request.form['address']
    try:
        lt=Lecturer().update_info(name,mail,phone,session['username'],address)
    except Exception as e:
        error_message = f"Error updating profile: {str(e)}"
        return render_template('lecturer_profile.html', error_message=error_message,profile=lt)
    return redirect('\lecturer_profile')

#update_grade
@app.route('/update_grade')
def update_grade():
    return render_template('update_grade.html',list_class=Lecturer().get_list_class(session['username']),list_class_previous=Lecturer().get_list_class_previous(session['username']),l_att_st=Lecturer().get_list_attendance_st(session['username']))

@app.route('/choose_student',methods=['POST'])
def choose_student():
    scheduleid=request.form['scheduleid']
    session['scheduleid']=scheduleid
    session['courseid']=request.form['courseid']
    session['semester']=request.form['semester']
    l_grade_st=Lecturer().get_list_student_class_grade(session['semester'],session['courseid'],session['username'])
    list_student=Lecturer().get_list_student_class(scheduleid)
    combined_list = []
    used_students = set()

    for student in list_student:
        for grade in l_grade_st:
            if grade['Student ID'] == student['Student ID']:
                combined_list.append({**grade, **student})
                used_students.add(student['Student ID'])
        if student['Student ID'] not in used_students:
            combined_list.append(student)       
        used_students = set()
    return render_template('update_grade.html',list_class=Lecturer().get_list_class(session['username']),list_class_previous=Lecturer().get_list_class_previous(session['username']),list_student=combined_list,l_att_st=Lecturer().get_list_attendance_st(session['username']))

@app.route('/input_grade',methods=['POST'])
def input_grade():
    conn=DatabaseConnector('lt').connect()
    cursor=conn.cursor()
    c=0
    st_list=Lecturer().get_list_student_class(session['scheduleid'])
    for student in st_list:
        studentid = student['Student ID']
        
        process_str = request.form.get('process_{}'.format(studentid))        
        if process_str:
            try:
                process = float(process_str)
            except ValueError:
                # handle the case where the input is not a valid float
                process = None
        else:
            process = None
                    
        mid_str = request.form.get('mid_{}'.format(studentid))
        if mid_str:
            try:
                mid = float(mid_str)
            except ValueError:
                # handle the case where the input is not a valid float
                mid = None
        else:
            mid = None
                    
        final_str = request.form.get('final_{}'.format(studentid))
        if final_str:
            try:
                final = float(final_str)
            except ValueError:
                # handle the case where the input is not a valid float
                final = None
        else:
            final = None      
        cursor.execute("select * from grade where studentid=%s and courseid=%s and semester=%s",(studentid,session['courseid'],session['semester']))
        result=cursor.fetchone()
        
        if process is None or mid is None or final is None:
            avg=0
        else:
            avg=process*0.2 + mid*0.3 + final*0.5
        
        if result:
            query="update grade set process=%s,mid=%s,final=%s,avg=%s where studentid=%s and courseid=%s and semester=%s"
            cursor.execute(query,(process,mid,final,avg,studentid,session['courseid'],session['semester']))
        else:
            query="insert into grade (studentid,courseid,semester,lecturerid,process,mid,final,avg) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,(studentid,session['courseid'],session['semester'],session['username'],process,mid,final,avg))
        conn.commit()
        if cursor.rowcount > 0:
            c+=1
    if c>0:
        message="success"
    else:
        message=f"Failed to update grades"
    # Retrieve the updated combined_list from the database
    l_grade_st = Lecturer().get_list_student_class_grade(session['semester'], session['courseid'], session['username'])
    list_student = Lecturer().get_list_student_class(session['scheduleid'])
    
    combined_list = []
    used_students = set()

    for student in list_student:
        for grade in l_grade_st:
            if grade['Student ID'] == student['Student ID']:
                combined_list.append({**grade, **student})
                used_students.add(student['Student ID'])
        if student['Student ID'] not in used_students:
            combined_list.append(student)
        used_students = set()
    
    cursor.close()
    conn.close()
    return render_template('update_grade.html',list_class=Lecturer().get_list_class(session['username']),list_student=combined_list,list_class_previous=Lecturer().get_list_class_previous(session['username']),message=message,l_att_st=Lecturer().get_list_attendance_st(session['username']))

@app.route('/down_report_grade', methods=['POST'])
def down_report_grade():
    course_id = request.form['courseid']
    semester = request.form['semester']
    columns = ['Student ID', 'Full name', 'Process','Mid','Final','Avg']
    results = Lecturer().get_list_student_class_previous(course_id,semester,session['username'])
    df = pd.DataFrame(results, columns=columns)
    excel_io=io.BytesIO()
    writer=pd.ExcelWriter(excel_io,engine='xlsxwriter')
    df.to_excel(writer,index=False,sheet_name='Grade')
    writer.close()
    excel_io.seek(0)
    return send_file(excel_io, download_name='Grade.xlsx', as_attachment=True)

def setstyle_table(table):
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Tahoma'),
        ('FONTSIZE', (0, 0), (-1, 0), 16),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 2), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Tahoma'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    return table
    
def draw_bar_chart(df): #for list student
    with pdf.PdfPages('bar_chart.pdf') as pdf_file:
        # Create a bar chart
        bins=[0,1,2,3,4,4.999,6,7,8,9,10]
        df['avg_bin'] = pd.cut(df['avg'], bins=bins, include_lowest=True)
        count = df['avg_bin'].value_counts().sort_index()
        bar_chart = count.plot(kind='bar',color=['red', 'red', 'red', 'red','red', 'blue', 'blue','blue', 'blue','blue'],figsize=(8.27, 11.69)) 
        plt.title('Distribution of Average Grades')
        plt.xlabel('Average Grades')
        plt.ylabel('Number of Students')
        plt.legend(['Number of Students'])
        plt.subplots_adjust(bottom=0.3)
        ax = plt.gca()
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        pdf_file.savefig()
        plt.clf()    
    return 'bar_chart.pdf'

def draw_pie_chart(df):
    with PdfPages('pie-chart.pdf') as pdf:
        # Create the second chart
        labels=['Fail','Pass']
        count_0_2 = df.query('0 < avg < 5')['avg'].count()
        count_2_4 = df.query('5 <= avg <= 10')['avg'].count()
        sizes = [count_0_2, count_2_4]
        col = ['red', 'blue']
        explode = (0, 0.1)
        fig2, ax2 = plt.subplots()
        ax2.set_title("Pass/Fail Percentage")
        ax2.pie(sizes, explode=explode, labels=labels, colors=col, autopct='%1.1f%%',shadow=False, startangle=90)
        ax2.axis('equal')
        
        # Adjust the figure size and subplots position
        plt.gcf().set_size_inches(8.27, 5.84) # half of A4 size
        plt.subplots_adjust(top=0.5) # move the chart position to the bottom half of the page

        # Add the second chart to the PDF file
        pdf.savefig()
        
        # Clear the current figure
        plt.clf()
    return 'pie-chart.pdf'

@app.route('/down_report_grade_pdf', methods=['POST'])
def down_report_grade_pdf():
    pdfmetrics.registerFont(TTFont('Tahoma', 'tahoma.ttf'))
    courseid = request.form.get('courseid')
    semester = request.form.get('semester')
    lecturerid = session['username']
    columns = ['studentID', 'name', 'process', 'mid', 'final', 'avg']
    results = Lecturer().get_list_student_class_previous(courseid, semester, session['username'])
    df = pd.DataFrame(results, columns=columns)
    #thông tin class lecturer
    session_info = [
        ['Course ID:', courseid],
        ['Semester:', semester],
        ['Lecturer ID:', lecturerid],
    ]
    session_table = Table(session_info)
    session_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Tahoma'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    try:
        # Tạo bảng từ dataframe
        title = [['GRADE REPORT']]
        data = [columns] + [[col if col is not None else '' for col in row] for row in df.values]
        table = Table(title + data)
        table=setstyle_table(table)
        merged_table = Table([
            [session_table],
            [table]
        ])    
        # Tạo tệp PDF mới và thêm bảng vào tệp
        buffer = io.BytesIO()
        doc = SimpleDocTemplate("table.pdf", pagesize=A4)
        doc.build([merged_table])
        data = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        # Load the two PDF files that you want to merge using PyPDF2
        char1=draw_bar_chart(df)
        char2=draw_pie_chart(df)
        pdf1 = PdfReader(open(char1, "rb"))
        pdf2 = PdfReader(open(char2, "rb"))
        pdf3 = PdfReader(open("table.pdf", "rb"))
        # Merge the two PDF files using PyPDF2
        merger = PdfMerger()
        merger.append(pdf1)
        merger.append(pdf2)
        merger.append(pdf3)

        buffer = io.BytesIO()
        merger.write(buffer)
        buffer.seek(0)
        return send_file(buffer, download_name='Report.pdf')
    except Exception as e:
        message=f"fail: {str(e)}"
        return render_template('update_grade.html',list_class=Lecturer().get_list_class(session['username']),list_class_previous=Lecturer().get_list_class_previous(session['username']),message=message)

@app.route('/update_attendance',methods=['POST'])
def update_attendance():  
    scheduleid=request.form['scheduleid']
    status=request.form['status']
    try:
        Lecturer().update_attendance(scheduleid,status)
        mess='success'
    except Exception as e:
        mess=f"fail: {str(e)}"
    return render_template('update_grade.html',list_class=Lecturer().get_list_class(session['username']),list_class_previous=Lecturer().get_list_class_previous(session['username']),Message=mess,l_att_st=Lecturer().get_list_attendance_st(session['username']))

@app.route('/down_report_att',methods=['POST'])
def down_report_att():
    scheduleid=request.form['scheduleid']
    l_att_st=Lecturer().get_list_attendance_st(scheduleid=scheduleid)
    df=pd.DataFrame(l_att_st)
    excel_io=io.BytesIO()
    writer=pd.ExcelWriter(excel_io,engine='xlsxwriter')
    df.to_excel(writer,sheet_name='attendance_info')
    writer.close()
    excel_io.seek(0)
    try: 
        Lecturer().delete_att_after_download(scheduleid)
        return send_file(excel_io,download_name='attendance_info.xlsx',as_attachment=True)
    except Exception as e:
        mess=f"fail: {str(e)}"
        return render_template('update_grade.html',list_class=Lecturer().get_list_class(session['username']),list_class_previous=Lecturer().get_list_class_previous(session['username']),Message=mess,l_att_st=Lecturer().get_list_attendance_st(session['username']))
