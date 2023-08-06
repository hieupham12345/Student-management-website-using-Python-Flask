from login import *
from lecturer import draw_pie_chart,draw_bar_chart,setstyle_table

class AdminUser:
    """
    class cho admin user
    """
    db_conn = None
    def __init__(self, staffID='', name='', dateOfBirth='', gender='', address='', email='', phoneNumber='', departmentID=''):
        self.staffID = staffID
        self.name = name
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.address = address
        self.email = email
        self.phoneNumber = phoneNumber
        self.departmentID = departmentID
        AdminUser.db_conn=DatabaseConnector('ad').connect()
    def get_info(self,staffID):
        """
        phương thức lấy thông tin cá nhân nhân viên
        -Input: staffID
        -Return: 1 dictionary chứa thông tin nhân viên
        """
        cursor = AdminUser.db_conn.cursor()
        if staffID:
            query = "SELECT * FROM adminuser WHERE staffid= %s"
            cursor.execute(query, (staffID,))
            result = cursor.fetchone()
            if result is not None:
                admin_info = AdminUser(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                return admin_info
    def update_info(self,  email=None, phoneNumber=None, staffID=None,address=None):# update for
        """
        phương thức cập nhập thông tin cá nhân:
        -Input: thông tin cần cập nhập (email, phone number, address, staffid)
        -Return: None
        """
        cursor=AdminUser.db_conn.cursor()
        if email:
            cursor.execute("UPDATE adminuser SET email=%s WHERE staffid=%s", (email, staffID))
            self.email = email
        if phoneNumber:
            cursor.execute("UPDATE adminuser SET phoneNumber=%s WHERE staffid=%s", (phoneNumber, staffID))
            self.phoneNumber = phoneNumber
        if address:
            cursor.execute("Update adminuser set address=%s where staffid=%s",(address,staffID))
            self.address=address
        AdminUser.db_conn.commit()
    def get_room(self): #lấy danh sách phòng
        """
        phương thức lấy danh sách phòng học/thi
        -input: noe
        -return: 1 danh sách các phòng học
        """
        cursor=AdminUser.db_conn.cursor()
        cursor.execute("select * from classroom")
        result=cursor.fetchall()
        l_room=[]
        for r in result:
            l_room.append(r[0])
        return l_room
    def get_test_schedule_list(self): #lấy danh sách lịch thi
        """
        phương thức lấy danh sách lịch thi
        -input: noe
        -return: 1 list dictionary chứa thông tin lịch thi
        """
        cursor=AdminUser.db_conn.cursor()
        cursor.execute("select scheduleID,course.coursename,course.courseid, time,classroomid from testschedule inner join course on testschedule.courseid=course.courseid")
        result=cursor.fetchall()
        test_list=[]
        for r in result:
            test={'Schedule ID':r[0] ,'Course name':r[1],'Course ID':r[2],'Time':r[3],'Classroom ID':r[4]}
            test_list.append(test)
        return test_list
    def get_list_student_test(self, scheduleid): #lấy danh sách sinh viên của của  schedule/testschedule
        """
        phương thức lấy danh sách sinh viên của thời khóa biểu/ lịch thi ( do lịch thi phụ thuộc thời khóa biểu)
        -input: scheduleID
        -return: 1 list dictionary chứa các thông tin sinh viên thỏa điều kiện
        """
        cursor = AdminUser.db_conn.cursor()
        cursor.execute("select student.studentid,name from student_schedule inner join student on student_schedule.studentid=student.studentid where scheduleid=%s",(scheduleid,))
        result = cursor.fetchall()
        ds_st=[]
        for r in result:
            st={'Student ID':r[0],'Name':r[1]}
            ds_st.append(st)
        return ds_st
    def insert_test_schedule(self,scheduleid,classroomID,time,courseid,lecturerid): #add lịch thi vào testschedule
        """
        phương thức insert vào bảng test schedule
        -input: scheduleID, classroomID, time, courseID, lecturerID
        -return: true nếu insert thành công, false nếu thất bại
        """
        cursor=AdminUser.db_conn.cursor()
        query = "insert into testschedule (scheduleID,classroomID,time,courseid,lecturerid) values (%s,%s,%s,%s,%s)"
        cursor.execute(query,(scheduleid,classroomID,time,courseid,lecturerid,))
        if cursor.rowcount==1:
            AdminUser.db_conn.commit()
            return True
        return False       
    def get_test_from_schedule(self): #lấy danh sách thời khóa biểu để chọn thêm  vào testschedule
        """
        lấy danh sách thời khóa biểu để chọn thêm  vào testschedule (do test schedule phụ thuộc schedule)
        -input: none
        -return: 1 list dictionary chứa thông tin thời khóa biểu        
        """
        cursor=AdminUser.db_conn.cursor()
        cursor.execute("select distinct scheduleid,courseid,day,time from schedule where scheduleid not in (select scheduleid from testschedule)")
        result=cursor.fetchall()
        ds_test=[]
        for r in result:
            test={'Schedule ID': r[0],'Course ID':r[1],'Day':r[2],'Time':r[3]}
            ds_test.append(test)
        return ds_test
    def delete_from_test_schedule(self,scheduleid): #xóa lịch thi khỏi testschedule
        """
        phương thức xóa lịch thi
        -input: scheduleID
        -return: none
        """
        cursor=AdminUser.db_conn.cursor()
        cursor.execute("delete from testschedule where scheduleid=%s",(scheduleid,))
        AdminUser.db_conn.commit()   
    def get_schedule(self):#get danh sách schedule
        """
        phương thức lấy danh sách thời khóa biểu
        -input: none
        -return: 1 list dictionary chứa thông tin thời khóa biểu
        """
        cursor=AdminUser.db_conn.cursor()
        query="select  scheduleid,courseid,day,time,classroomid,lecturerid,semester from schedule"
        cursor.execute(query)
        result=cursor.fetchall()
        l_schedule=[]
        for r in result:
            schedule=Schedule(r[0],r[1],r[2],r[3],r[4],r[5],r[6]).__dict__
            l_schedule.append(schedule)
        return l_schedule
    def get_list_schedule_input(self):
        """
        lấy 1 table gồm: facultyID, courseID, courseName,lecturerID,lecturerName để chọn add schedule (chọn giảng viên, môn học phải chung khoa)
        -input: none
        -return: 1 list dictionary chứa các thông tin thỏa điều kiện
        """
        cursor=AdminUser().db_conn.cursor()
        query="select course.facultyid,facultyname,courseid,coursename,lecturer.lecturerid,lecturer.name from course inner join lecturer on course.facultyid=lecturer.facultyid inner join faculty on lecturer.facultyid=faculty.facultyID"
        cursor.execute(query)
        result=cursor.fetchall()
        l_add=[]
        for r in result:
            a={'Faculty ID':r[0],'Faculty Name':r[1],'Course ID':r[2],'Course Name':r[3],'Lecturer ID':r[4],'Lecturer Name':r[5]}
            l_add.append(a)
        return l_add
    def insert_schedule(self,courseid,date,time,classroomid,lecturerid,semester): #insert schedule
        """
        phương thức insert vào schedule
        -input: courseid, date, time, classroomID, lecturerID, semester
        -return: true nếu insert thành công, false nếu thất bại
        """
        cursor=AdminUser.db_conn.cursor()
        cursor.execute("select max(scheduleid) from schedule")
        result=cursor.fetchone()
        id=result[0]
        scheduleid=id[0:2]+str(int(id[2:])+1)
        query="insert into schedule (scheduleid,courseid,day,time,classroomid,lecturerid,semester) values (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(scheduleid,courseid,date,time,classroomid,lecturerid,semester,))
        if cursor.rowcount==1:
            AdminUser.db_conn.commit()
            return True
        return False     
    def add_student_schedule(self,studentid,scheduleid): #thêm sinh viên vào schedule
        """
        phương thức thêm sinh viên vào thời khóa biểu
        -input: studentID, scheduleID
        -return: true nếu insert thành công, false nếu thất bại
        """
        cursor=AdminUser.db_conn.cursor()
        query="insert into student_schedule (studentid,scheduleid) values (%s,%s)"
        cursor.execute(query,(studentid,scheduleid))
        if cursor.rowcount>=1:
            AdminUser.db_conn.commit()
            return True
        return False
    def delete_student_schedule(self,scheduleid,studentid=''): #xóa từng sinh viên khỏi schedule
        """
        phương thức delete sinh viên từ thời khóa biểu
        -input: scheduleID, studentID
        -return: true nếu xóa thành công, false nếu thất bại
        """
        cursor=AdminUser.db_conn.cursor()
        if studentid:
            query="delete from student_schedule where studentid=%s and scheduleid = %s"
            cursor.execute(query,(studentid,scheduleid,))
        else:
            query="delete from student_schedule where scheduleid = %s"
            cursor.execute(query,(scheduleid,))
        if cursor.rowcount>=1:
            AdminUser.db_conn.commit()
            return True
        return False
    def get_scheduleinfo_by(self, scheduleid): #lấy thông tin schedule để xuất file excel
        """
        phương thức lấy thông tin thời khóa biểu để xuất file excel
        -input: scheduleID
        -return: 1 dictionary chứa thông tin thời khóa biểu theo scheduleID
        """
        cursor = AdminUser.db_conn.cursor()
        query = "SELECT schedule.courseid, coursename, day, time, classroomID, name, semester FROM course INNER JOIN schedule ON course.courseid=schedule.courseid INNER JOIN lecturer ON schedule.lecturerid=lecturer.lecturerid WHERE scheduleid=%s"
        cursor.execute(query, (scheduleid,))
        r = cursor.fetchone()
        if r:
            s_ = {'Course ID': r[0], 'Course Name': r[1], 'Day': r[2], 'Time': r[3], 'Classroom ID': r[4], 'Lecturer Name': r[5], 'Semester': r[6]}
            return s_
        else:
            return {}
    def delete_schedule(self,scheduleid): #xóa schedule sau khi xóa từng record của table student_schedule
        """
        phương thức xóa schedule sau khi xóa từng record của table student_schedule
        -input: scheduleID
        -return: true nếu xóa thành công, false nếu thất bại
        """
        cursor=AdminUser.db_conn.cursor()
        query="delete from schedule where scheduleid=%s"
        cursor.execute(query,(scheduleid,))
        if cursor.rowcount>=1:
            AdminUser.db_conn.commit()
            return True
        return False
    def search_student(self,studentid='',studentname='',dob='',gender='',address='',email='',phone='',classid='',facultyid=''):
        """
        phương thức search student theo toàn bộ thông tin cá nhân, tìm kiếm gần đúng
        -input: 1 hoặc nhiều thông tin cá nhân
        -return: 1 list dictionary chứa các thông tin sinh viên thỏa điều kiện
        """
        cursor=AdminUser.db_conn.cursor()
        query = "SELECT student.*,facultyid FROM student inner join faculty_class on student.classid=faculty_class.classid WHERE 1=1"
        conditions = []
        if studentid:
            conditions.append(f"studentid LIKE '%{studentid}%'")
        if studentname:
            conditions.append(f"name LIKE '%{studentname}%'")
        if dob:
            conditions.append(f"dateofbirth LIKE '%{dob}%'")
        if gender:
            conditions.append(f"gender LIKE '%{gender}%'")
        if address:
            conditions.append(f"address LIKE '%{address}%'")
        if email:
            conditions.append(f"email LIKE '%{email}%'")
        if phone:
            conditions.append(f"phonenumber LIKE '%{phone}%'")
        if classid:
            conditions.append(f"student.classid LIKE '%{classid}%'")
        if facultyid:
            conditions.append(f"facultyid LIKE '%{facultyid}%'")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        cursor.execute(query)
        result = cursor.fetchall()
        st_list=[]
        for r in result:
            re={'studentID':r[0],'name':r[1],'dateOfBirth':r[2],'gender':r[3],'address':r[4],'email':r[5],'phoneNumber':r[6],'classID':r[7],'facultyID':r[8]}
            st_list.append(re)
        return st_list
    def get_list_class_student(self):
        """
        lấy danh sách lớp sinh viên từ table studentclass
        -input: none
        -return: 1 list chứa toàn bộ classID
        """
        cursor=AdminUser.db_conn.cursor()
        query="select classid from studentclass"
        cursor.execute(query)
        result=cursor.fetchall()
        l_class=[]
        for r in result:
            re=r[0]
            l_class.append(re)
        return l_class
    def get_list_faculty(self):
        """
        lấy danh sách khoa
        -input: none
        -return: 1 list chứa toàn bộ facultyID
        """
        cursor=AdminUser.db_conn.cursor()
        query="select facultyid from faculty"
        cursor.execute(query)
        result=cursor.fetchall()
        l_faculty=[]
        for r in result:
            re=r[0]
            l_faculty.append(re)
        return l_faculty    
    def search_grade(self,studentid='',name='',courseid='',semester='',lecturerid='',classid='',facultyid=''):
        """
        phương thức search student theo một số thông tin cá nhân để lọc danh sách điểm số, tìm kiếm gần đúng
        -input: 1 hoặc nhiều thông tin cá nhân
        -return: 1 list dictionary chứa các thông tin sinh viên thỏa điều kiện
        """
        cursor=AdminUser.db_conn.cursor()
        query="select student.name,student.classid,facultyid,grade.* from student inner join grade on student.studentid=grade.studentid inner join faculty_class on student.classid=faculty_class.classid where 1=1"
        conditions=[]
        if studentid:
            conditions.append(f"student.studentid LIKE '%{studentid}%'")
        if name:
            conditions.append(f"name LIKE '%{name}%'")
        if facultyid:
            conditions.append("facultyid = '{}'".format(facultyid))
        if classid:
            conditions.append("student.classid = '{}'".format(classid))
        if courseid:
            conditions.append(f"courseid LIKE '%{courseid}%'")
        if semester:
            conditions.append(f"semester LIKE '%{semester}%'")
        if lecturerid:
            conditions.append(f"lecturerid  LIKE '%{lecturerid}%'")

        if conditions:
            query += " AND " + " AND ".join(conditions)
        cursor.execute(query)
        result=cursor.fetchall()
        st_list=[]
        for r in result:
            st={'StudentID':r[3],'Name':r[0],'ClassID':r[1],'FacultyID':r[2],'CourseID':r[4],'Semester':r[5],'LecturerID':r[6],'process':r[7],'mid':r[8],'final':r[9],'avg':r[10]}
            st_list.append(st)
        return st_list




@app.route('/ad_user_profile')
def ad_user_profile():
    """
    hàm hướng tới profile user
    -input: none
    -return: page ad_user_profile.html
    """
    return render_template('ad_user_profile.html',profile=AdminUser().get_info(session['username']))

@app.route('/ad_user_home')
def ad_user_home():
    """
    hàm hướng tới dashboard của user
    -input: none
    -return: page ad_user_home.html
    """
    return render_template('ad_user_home.html')

#update info
@app.route('/ad_user_update_info',methods=['POST'])
def ad_user_update_info():
    """
    hàm cập nhập thông tin
    -input: mail, phone, address
    -return: message thông báo thành công hay thất bại
    """
    mail = request.form['mail']
    phone = request.form['phone']
    address=request.form['address']
    try:
        AdminUser().update_info(mail,phone,session['username'],address)
    except Exception as e:
        error_message = f"Error updating profile: {str(e)}"
        return render_template('ad_user_profile.html', error_message=error_message,profile=AdminUser().get_info(session['username']))
    return redirect('/ad_user_profile')

#test_schedule_manage
@app.route('/test_schedule_manage')
def test_schedule_manage():
    """
    hàm hướng tới page schedule_manage
    -input: none
    -return: page test_schedule_manage.html
    """
    return render_template('test_schedule_manage.html',test_list=AdminUser().get_test_schedule_list(),test_list_schedule=AdminUser().get_test_from_schedule(),l_room=AdminUser().get_room(),l_lt=AdminUser().get_lecturerid())


@app.route('/add_test_schedule',methods=['POST'])
def add_test_schedule():
    """
    hàm thêm lịch thi mới
    -input: scheduleID, courseID, date, time, lecturerID
    -return: message báo thành công hay thất bại
    """
    selected = request.form['test']
    scheduleid,courseid= selected.split(',')
    room_test=request.form['room']
    time_test=request.form['date']+' '+request.form['time']
    lecturerid=request.form['lecturer']
    try:
        a=AdminUser().insert_test_schedule(scheduleid,room_test,time_test,courseid,lecturerid)
        mess='add success'
    except Exception as e:
        mess = f"Error adding: {str(e)}"
    return render_template('test_schedule_manage.html',Message=mess,test_list=AdminUser().get_test_schedule_list(),test_list_schedule=AdminUser().get_test_from_schedule(),l_room=AdminUser().get_room(),l_lt=AdminUser().get_lecturerid())

@app.route('/list_student_test',methods=['POST'])
def list_student_test():
    """
    hàm lấy danh sách sinh viên của 1 lịch thi 
    -input: scheduleID
    -return: page test_schedule_manage.html với danh sách sinh viên tương ứng
    """
    scheduleid=request.form['scheduleid']
    return render_template('test_schedule_manage.html',test_list=AdminUser().get_test_schedule_list(),test_list_schedule=AdminUser().get_test_from_schedule(),l_room=AdminUser().get_room(),st_list=AdminUser().get_list_student_test(scheduleid))

@app.route('/delete_test_schedule',methods=['POST'])
def delete_test_schedule():
    """
    hàm xóa lịch thi
    -input: scheduleID
    -return: message báo thành công hay thất bại
    """
    scheduleid=request.form['scheduleid']
    try:
        a=AdminUser().delete_from_test_schedule(scheduleid)
        mess='Success'
    except Exception as e:
        mess=f"Error : {str(e)}"
    return render_template('test_schedule_manage.html',Message=mess,test_list=AdminUser().get_test_schedule_list(),test_list_schedule=AdminUser().get_test_from_schedule(),l_room=AdminUser().get_room())

@app.route('/schedule_manage')
def schedule_manage():
    """
    hàm hướng tới page schedule_manage
    -input: none
    -return: page schedule_manage.html
    """
    return render_template('schedule_manage.html',l_schedule=AdminUser().get_schedule(),list_schedule_input=AdminUser().get_list_schedule_input(),l_room=AdminUser().get_room())

@app.route('/input_schedule',methods=['POST'])
def input_schedule():
    """
    hàm thêm 1 lịch thời khóa biểu mới
    -inputL courseID, lecturerID, classroomID, date, time, semester
    -return: message báo thêm thành công hay thất bại
    """
    selected=request.form['schedule']
    courseid,lecturerid=selected.split(',')
    classroomid=request.form['room']
    date=request.form['date']
    time=request.form['time']
    semester=request.form['semester']
    try:
        a=AdminUser().insert_schedule(courseid,date,time,classroomid,lecturerid,semester)
        mess="Success"
    except Exception as e:
        mess=f"Fail, please try again: {str(e)}"
    return render_template('schedule_manage.html',Message=mess,l_schedule=AdminUser().get_schedule(),list_schedule_input=AdminUser().get_list_schedule_input(),l_room=AdminUser().get_room())

@app.route('/list_student_schedule',methods=['POST'])
def list_student_schedule():
    """
    hàm lấy danh sách sinh viên của 1 lịch thời khóa biểu
    -input: scheduleID
    -return: page schedule_manage.html với danh sách sinh viên tương ứng
    """
    scheduleid=request.form['scheduleid']
    session['scheduleid']=scheduleid
    st_list=AdminUser().get_list_student_test(scheduleid)
    if st_list is None:
        st_list='#'
    return render_template('schedule_manage.html',l_schedule=AdminUser().get_schedule(),list_schedule_input=AdminUser().get_list_schedule_input(),l_room=AdminUser().get_room(),st_list=st_list)

@app.route('/add_student_schedule',methods=['POST'])
def add_student_schedule():
    """
    hàm thêm 1 sinh viên mới vào lịch thời khóa biểu
    -input: studentID, scheduleID
    -return: message báo thành công hay thất bại
    """
    studentid=request.form['studentid']
    scheduleid=session.get('scheduleid')
    if scheduleid is None:
        mess='select schedule first'
        return render_template('schedule_manage.html',l_schedule=AdminUser().get_schedule(),list_schedule_input=AdminUser().get_list_schedule_input(),l_room=AdminUser().get_room(),Message=mess)
    else:
        try:
            AdminUser().add_student_schedule(studentid,scheduleid)
            mess='success'
        except Exception as e:
            mess=f"fail: {str(e)}"
        return render_template('schedule_manage.html',l_schedule=AdminUser().get_schedule(),list_schedule_input=AdminUser().get_list_schedule_input(),l_room=AdminUser().get_room(),st_list=AdminUser().get_list_student_test(scheduleid),Message=mess)

@app.route('/delete_student_schedule',methods=['POST'])
def delete_student_schedule():
    """
    hàm delete sinh viên khỏi lịch thời khoa biểu
    -input: studentID, scheduleID
    -return: message báo thành công hay thất bại
    """
    studentid=request.form['studentid']
    scheduleid=session['scheduleid']
    try:
        AdminUser().delete_student_schedule(scheduleid,studentid)
        mess='success'
    except Exception as e:
        mess=f"fail: {str(e)}"
    return render_template('schedule_manage.html',l_schedule=AdminUser().get_schedule(),list_schedule_input=AdminUser().get_list_schedule_input(),l_room=AdminUser().get_room(),st_list=AdminUser().get_list_student_test(scheduleid),Message=mess)

@app.route('/download_schedule_student')
def download_schedule_student():
    """
    hàm download lịch thời khóa biểu file excel
    -input: none
    -return: file excel
    """
    schedule_info=AdminUser().get_scheduleinfo_by(session['scheduleid'])
    try:
        student_list = AdminUser().get_list_student_test(session['scheduleid'])
        data = {
            'Student ID': [x['Student ID'] for x in student_list],
            'Name': [x['Name'] for x in student_list],
        }
        df = pd.DataFrame(data)
        schedule_df = pd.DataFrame.from_dict(schedule_info, orient='index', columns=['Value']).reset_index().rename(columns={'index': 'Key'})
        df.index.name = 'Key'
        df = pd.concat([schedule_df, df])  # Add schedule_df as the first row
        excel_io = io.BytesIO()
        writer = pd.ExcelWriter(excel_io, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Schedule')
        writer.close()  # Close the workbook
        excel_io.seek(0)
        return send_file(excel_io, download_name='schedule.xlsx', as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/delete_schedule')
def delete_schedule():
    """
    hàm xóa lịch thời khóa biểu
    -input: scheduleID
    -return: message báo thành công hay thất bại
    """
    scheduleid=session['scheduleid']
    st_list=AdminUser().get_list_student_test(scheduleid)
    if len(st_list)>0:
        AdminUser().delete_student_schedule(scheduleid)
    try:
        AdminUser().delete_schedule(scheduleid)
        mess='delete success'
    except Exception as e:
        mess=f'fail to delete. str{e}'
    return render_template('schedule_manage.html',l_schedule=AdminUser().get_schedule(),list_schedule_input=AdminUser().get_list_schedule_input(),l_room=AdminUser().get_room(),Message=mess,    st_list=AdminUser().get_list_student_test(scheduleid))

@app.route('/student_manage')
def student_manage():
    """
    hàm hướng tới page student_manage
    -input: none
    -return: page student_manage với thông tin danh sách lớp và khoa
    """
    l_class=AdminUser().get_list_class_student()
    l_faculty=AdminUser().get_list_faculty()
    return render_template('student_manage.html',l_class=l_class,l_faculty=l_faculty)

@app.route('/search_student',methods=['POST'])
def search_student():
    """
    hàm search student
    -input: 1 hoặc nhiều thông tin cá nhân sinh viên
    -return: page student_manage.html với danh sách sinh viên đã tìm thỏa điều kiện
    """
    if request.method == 'POST':
        session['student_id'] = request.form['studentId']
        session['student_name'] = request.form['studentName']
        session['date_of_birth'] = request.form['dateOfBirth']
        session['gender'] = request.form['gender']
        session['address'] = request.form['address']
        session['email'] = request.form['email']
        session['phone_number'] = request.form['phoneNumber']
        session['selected_class'] = request.form['class']
        session['selected_faculty'] = request.form['faculty']
        st_list = AdminUser().search_student(session.get('student_id'),session.get('student_name'),session.get('date_of_birth'),session.get('gender'),session.get('address'),session.get('email'),session.get('phone_number'),session.get('selected_class'),session.get('selected_faculty'))
        return render_template('student_manage.html',st_list=st_list,l_faculty=AdminUser().get_list_faculty(),l_class=AdminUser().get_list_class_student()
)

@app.route('/download_student_search')
def download_student_search():
    """
    hàm download file excel chứa thông tin sinh viên tìm qua search function
    -input: none
    -return: file excel
    """
    try:
        st_list = AdminUser().search_student(session.get('student_id'),session.get('student_name'),session.get('date_of_birth'),session.get('gender'),session.get('address'),session.get('email'),session.get('phone_number'),session.get('selected_class'),session.get('selected_faculty'))
        df=pd.DataFrame(st_list)
        df['dateOfBirth'] = df['dateOfBirth'].dt.tz_localize(None)
        excel_io=io.BytesIO()
        Writer=pd.ExcelWriter(excel_io,engine='xlsxwriter')
        df.to_excel(Writer,index=False,sheet_name='List student')
        Writer.close()  # Close the workbook
        excel_io.seek(0)
        return send_file(excel_io, download_name='List student.xlsx', as_attachment=True)
    except Exception as e:
        mess=f"fail. str{e}"
        return render_template('student_manage.html',l_class=AdminUser().get_list_class_student(),l_faculty=AdminUser().get_list_faculty(),Message=mess)

@app.route('/grade_manage')
def grade_manage():
    """
    hàm hướng tới page grade_manage.html
    -input: none
    -return: page grade_manage.html với thông tin danh sách lớp học sinh viên và khoa
    """
    return render_template('grade_manage.html',l_class=AdminUser().get_list_class_student(),l_faculty=AdminUser().get_list_faculty())

@app.route('/search_student_grade',methods=['POST'])
def search_student_grade():
    """
    hàm search student với điểm số
    -input: 1 hoặc nhiều thông tin cá nhân sinh viên
    -return: page student_manage.html với danh sách sinh viên đã tìm thỏa điều kiện
    """
    if request.method == 'POST':
        session['student_id'] = request.form['studentid']
        session['student_name'] = request.form['studentname']
        session['courseid']=request.form['courseid']
        session['semester']=request.form['semester']
        session['lecturerid']=request.form['lecturerid']
        session['selected_class'] = request.form['class']
        session['selected_faculty'] = request.form['faculty']
        st_list_gr = AdminUser().search_grade(session.get('student_id'),session.get('student_name'),session.get('courseid'),session.get('semester'),session.get('lecturerid'),session.get('selected_class'),session.get('selected_faculty'))
        return render_template('grade_manage.html',l_class=AdminUser().get_list_class_student(),l_faculty=AdminUser().get_list_faculty(),st_list=st_list_gr)

@app.route('/download_student_grade_data')
def download_student_grade_data():
    """
    hàm download file excel chứa thông tin điểm số sinh viên tìm qua search function
    -input: none
    -return: file excel
    """
    column=['StudentID','Name','ClassID','FacultyID','CourseID','Semester','LecturerID','process','mid','final','avg']
    st_list_gr = AdminUser().search_grade(session.get('student_id'),session.get('student_name'),session.get('courseid'),session.get('semester'),session.get('lecturerid'),session.get('selected_class'),session.get('selected_faculty'))
    df=pd.DataFrame(st_list_gr,columns=column)
    excel_io=io.BytesIO()
    writer=pd.ExcelWriter(excel_io,engine='xlsxwriter')
    df.to_excel(writer,index=False,sheet_name='Grade')
    writer.close()
    excel_io.seek(0)
    return send_file(excel_io,download_name='Grade.xlsx',as_attachment=True)

@app.route('/download_student_grade_data_pdf')
def download_student_grade_data_pdf():
    """
    hàm download file report pdf chứa thông tin điểm số sinh viên tìm qua search function
    -input: none
    -return: file pdf
    """
    column=['StudentID','Name','ClassID','FacultyID','CourseID','Semester','LecturerID','process','mid','final','avg']
    st_list_gr = AdminUser().search_grade(session.get('student_id'),session.get('student_name'),session.get('courseid'),session.get('semester'),session.get('lecturerid'),session.get('selected_class'),session.get('selected_faculty'))
    df=pd.DataFrame(st_list_gr,columns=column)
    pdfmetrics.registerFont(TTFont('Tahoma', 'tahoma.ttf'))
    title=[['GRADE REPORT']]
    data=[column]+[[col if col is not None else '' for col in row] for row in df.values]
    table=Table(title + data)

    table=setstyle_table(table)
    
    buffer=io.BytesIO()
    doc=SimpleDocTemplate("table1.pdf",pagesize=A3)
    doc.build([table])
    data = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    #bar_chart cho phân bố điểm
    bar_char=draw_bar_chart(df)
    #pie_chart cho fail/pass
    pie_char=draw_pie_chart(df)
    
    pdf1=PdfReader(open(bar_char,"rb"))
    pdf2=PdfReader(open(pie_char,"rb"))
    pdf3=PdfReader(open("table1.pdf","rb"))
    mergePdf=PdfMerger()
    mergePdf.append(pdf1)
    mergePdf.append(pdf2)
    mergePdf.append(pdf3)
    
    buffer=io.BytesIO()
    mergePdf.write(buffer)
    buffer.seek(0)
    return send_file(buffer,download_name='grade.pdf')


