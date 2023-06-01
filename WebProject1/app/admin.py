from login import *
from ad_user import AdminUser
from lecturer import Lecturer
from student import Course

class Admin:
    """
    class chứa phương thức của admin
    """
    db_conn=None
    def __init__(self):
        Admin.db_conn=DatabaseConnector('adminadmin').connect()
    def get_max_studentid(self): #for input
        """
        phương thức lấy studentID lớn nhất hiện tại (để tự động cập nhập studentID khi thêm sinh viên mới)
        -input: note
        -return: max studentID
        """
        cursor = Admin.db_conn.cursor()
        query = "SELECT MAX(studentid) FROM student;"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        if result is None:
            new_id = 'st000001'
        else:
            new_id = 'ST' +'0'*(6-len(str(int(result[2:])+1)))+ str(int(result[2:]) + 1)
        return new_id
    def get_max_lecturerid(self): #for input
        """
        phương thức lấy lecturerID lớn nhất hiện tại (để tự động cập nhập lecturerID khi thêm sinh viên mới)
        -input: note
        -return: max lecturerID
        """
        cursor = Admin.db_conn.cursor()
        query = "SELECT MAX(lecturerid) FROM lecturer;"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        if result is None:
            new_id = 'lt000001'
        else:
            new_id = 'LT' +'0'*(6-len(str(int(result[2:])+1)))+ str(int(result[2:]) + 1)
        return new_id
    def get_faculty_class(self):
        """
        phương thức lấy danh sách khoa và lớp học tương ứng theo cặp khoa - lớp học
        -input: note
        -return: 1 list dictionary chứa thông tinh tương ứng
        """
        cursor=Admin.db_conn.cursor()
        cursor.execute("select studentclass.classid,facultyname,faculty_class.facultyID from studentclass inner join faculty_class on studentclass.classid=faculty_class.classid inner join faculty on faculty_class.facultyid=faculty.facultyid")
        result=cursor.fetchall()
        l_fa_class=[]
        for r in result:
            fc={'Class ID':r[0],'Faculty Name':r[1],'Faculty ID':r[2]}
            l_fa_class.append(fc)
        return l_fa_class
    def insert_student(self,studentID='', name='', dateOfBirth='', gender='', address='', email='', phoneNumber='', classID=''):
        """
        phương thức insert sinh viên mới
        -input: thông tin sinh viên
        -return: true nếu insert thành công, false nếu thất bại
        """
        cursor=Admin.db_conn.cursor()
        query="insert into student (studentid,name,dateofbirth,gender,address,email,phonenumber,classid) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(studentID,name,dateOfBirth,gender,address,email,phoneNumber,classID,))
        if cursor.rowcount>=1:
            Admin.db_conn.commit()
            return True
        return False
    def create_account(self,id,user_mail): #create account and send mail
        """
        phương thức tự động tạo account mới (insert vào table account) và gửi mail cho user sau khi admin insert new user
        -input: id, user_mail
        -return: true nếu gửi mail thành công, false nếu thất bại
        """
        cursor=Admin.db_conn.cursor()
        random_password=Reset_password().generate_password()
        query="insert into account (username,password) values (%s,sha2(%s,256))"
        cursor.execute(query,(id,random_password,))
        if cursor.rowcount>=1:
            Admin.db_conn.commit()
            msg=Message('New account',sender=mail_user,recipients=[user_mail])
            msg.body=f'You account has been created. Username: {id}, password: {random_password}. Please login at http://127.0.0.1:5000/login and change password imediately'
            mail.send(msg)
            del random_password
            return True
        return False
    def delete_student(self, id):
        """
        phương thức xóa sinh viên
        -input: studentID
        -return: true nếu xóa thành công, false nếu thất bại
        """
        cursor = Admin.db_conn.cursor()
        try:
            cursor.execute("START TRANSACTION")
            query = "DELETE FROM student WHERE studentid=%s"
            cursor.execute(query, (id,))
            query1 = "DELETE FROM account WHERE username=%s"
            cursor.execute(query1, (id,))
            if cursor.rowcount >= 1:
                Admin.db_conn.commit()
                return True
            else:
                return Exception("Not success")
        except Exception as e:
            Admin.db_conn.rollback()
            return str(e)

    def insert_lecturer(self,lecturerID='', name='', dateOfBirth='', gender='', address='', email='', phoneNumber='',  facultyID=''):
        """
        phương thức thêm 1 giảng viên mới:
        -input: thông tin cá nhân giảng viên
        -return: true nếu insert thành công, false nếu thất bại
        """
        cursor=Admin.db_conn.cursor()
        query="insert into lecturer (lecturerid,name,dateofbirth,gender,address,email,phonenumber,facultyid) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(lecturerID,name,dateOfBirth,gender,address,email,phoneNumber,facultyID,))
        if cursor.rowcount>=1:
            Admin.db_conn.commit()
            return True
        return False
    def delete_lecturer(self, id):
        """
        phương thức xóa giảng viên
        -input: studentID
        -return: true nếu xóa thành công, false nếu thất bại
        """
        cursor = Admin.db_conn.cursor()
        try:
            cursor.execute("START TRANSACTION")
            query = "DELETE FROM lecturer WHERE lecturerid=%s"
            cursor.execute(query, (id,))
            query1 = "DELETE FROM account WHERE username=%s"
            cursor.execute(query1, (id,))
            if cursor.rowcount >= 1:
                Admin.db_conn.commit()
                return True
            else:
                return Exception("Not success")
        except Exception as e:
            Admin.db_conn.rollback()
            return str(e)
    def search_lecturer(self,lecturerid='',studentname='',dob='',gender='',address='',email='',phone='',facultyid=''):
        """
        phương thức search giảng viên theo toàn bộ thông tin cá nhân, tìm kiếm gần đúng
        -input: 1 hoặc nhiều thông tin cá nhân
        -return: 1 list dictionary chứa các thông tin giảng viên thỏa điều kiện
        """
        cursor=AdminUser.db_conn.cursor()
        query = "SELECT * FROM lecturer WHERE 1=1"
        conditions = []
        if lecturerid:
            conditions.append(f"lecturerid LIKE '%{lecturerid}%'")
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
        if facultyid:
            conditions.append(f"facultyid LIKE '%{facultyid}%'")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        cursor.execute(query)
        result = cursor.fetchall()
        st_list=[]
        for r in result:
            re=Lecturer(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7])
            st_list.append(re.__dict__)
        return st_list
    def search_course(self,courseid='',coursename='',facultyid=''):
        """
        phương thức search môn học theo courseID, course name, facultyID, tìm kiếm gần đúng
        -input: 1 hoặc nhiều thông tin 
        -return: 1 list dictionary chứa các thông tin môn học thỏa điều kiện
        """
        cursor=Admin.db_conn.cursor()
        query="select * from course where 1=1"
        conditions=[]
        if courseid:
            conditions.append(f"courseid LIKE '%{courseid}%'")
        if coursename:
            conditions.append(f"coursename LIKE '%{coursename}%'")
        if facultyid:
            conditions.append("facultyid='{}'".format(facultyid))
        
        if conditions:
            query+=" AND " + " AND ".join(conditions)
        cursor.execute(query)
        result=cursor.fetchall()
        c_list=[]
        for r in result:
            course=Course(r[0],r[1],r[2],r[3],r[4],r[5],r[6])
            c_list.append(course)
        return c_list
    def add_course(self,courseid='',coursename='',facultyid='',credit='',description='',previous='',following=''):
        """
        phương thức thêm môn học mới
        -input: các thông tin môn học
        -return: true nếu thêm thành công, false nếu thất bại
        """
        cursor=Admin.db_conn.cursor()
        query="insert into course (courseid,coursename,facultyid,credit,description,previouscourse,followingcourse) values (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(courseid,coursename,facultyid,credit,description,previous,following,))
        if cursor.rowcount>=1:
            Admin.db_conn.commit()
            return True
        return False
    def delete_course(self,courseid):
        """
        phương thức xóa môn học 
        -input: courseID
        -return: true nếu xóa thành công, false nếu thất bại
        """
        cursor=Admin.db_conn.cursor()
        query="delete from course where courseid=%s"
        cursor.execute(query,(courseid,))
        if cursor.rowcount>=1:
            Admin.db_conn.commit()
            return True
        return False
    def backup_to_file(self):
        """
        phương thức lấy file back up database
        -input: none
        -return: none
        """
        cursor = Admin.db_conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        with open("backup.sql", "w",encoding="utf-8") as f:
            f.write("CREATE DATABASE IF NOT EXISTS database_name;\n")
            f.write("USE database_name;\n")
            for table in tables:
                table_name = table[0]
                cursor.execute("SELECT * FROM " + table_name)

                # Lấy tất cả các hàng từ kết quả truy vấn
                rows = cursor.fetchall()

                # Ghi lệnh để tạo bảng
                create_table_query = "SHOW CREATE TABLE " + table_name
                cursor.execute(create_table_query)
                create_table = cursor.fetchone()
                f.write(create_table[1] + ";\n")

                # Ghi từng hàng vào tệp
                for row in rows:
                    values = ", ".join("'" + str(value) + "'" for value in row)
                    insert_query = "INSERT INTO " + table_name + " VALUES (" + values + ")"
                    f.write(insert_query + ";\n")
            cursor.close()
    def send_file_mail(self, email):
        """
        phương thức gửi file back up qua mail
        -input: admin mail
        -return: none
        """
        msg = Message('Back up file', sender=mail_user, recipients=[email,])
        msg.body = 'File back up database'
        
        with open('backup.sql', 'rb') as f:
            data = f.read()
            msg.attach('backup.sql', 'application/octet-stream', data)
        mail.send(msg)


@app.route('/admin_home')
def admin_home():
    """
    hàm hướng đến admin_home
    -input: none
    -return: page admin_home.html 
    """
    return render_template('admin_home.html')

@app.route('/student_record_manage')
def student_record_manage():
    """
    hàm hướng đến student_record_manage
    -input: none
    -return: page student_record_manage.html 
    """
    return render_template('student_record_manage.html',l_class_fa=Admin().get_faculty_class(),st_id=Admin().get_max_studentid(),l_class=AdminUser().get_list_class_student(),l_faculty=AdminUser().get_list_faculty())

@app.route('/search_student_record',methods=['POST'])
def search_student_record():
    """
    hàm search student theo toàn bộ thông tin cá nhân, tìm kiếm gần đúng
    -input: 1 hoặc nhiều thông tin cá nhân
    -return: page student_record_manage và danh sách sinh viên thỏa điều kiện
    """
    if request.method == 'POST':
        student_id = request.form['studentId']
        student_name = request.form['studentName']
        date_of_birth = request.form['dateOfBirth']
        gender = request.form['gender']
        address = request.form['address']
        email = request.form['email']
        phone_number = request.form['phoneNumber']
        selected_class = request.form['class']
        selected_faculty = request.form['faculty']
        st_list =AdminUser().search_student(student_id, student_name, date_of_birth, gender, address, email, phone_number, selected_class, selected_faculty)
        return render_template('student_record_manage.html',st_list=st_list,l_class_fa=Admin().get_faculty_class(),st_id=Admin().get_max_studentid(),l_class=AdminUser().get_list_class_student(),l_faculty=AdminUser().get_list_faculty())


@app.route('/input_student',methods=['POST'])
def input_student(): #cần insert student, account, send_mail
    """
    hàm thêm sinh viên mới
    -input: thông tin cá nhân sinh viên
    -return: message thông báo thêm thành công hay thất bại
    """
    studentid=request.form['studentid']
    name=request.form['name']
    dob=request.form['dob']
    gender=request.form['gender']
    mail=request.form['email']
    selected=request.form['cl_faculty']
    classid,facultyid=selected.split(',')
    try:
        Admin().insert_student(studentID=studentid,name=name,dateOfBirth=dob,gender=gender,email=mail,classID=classid)
        try:
            Admin().create_account(studentid,mail) ### mail từ request         
            mess='success. Account have been sended to user.'
        except Exception as e:
            mess=f'Fail. {str(e)}'
    except Exception as e:
        mess=f"Fail. {str(e)}"        
    return render_template('student_record_manage.html',l_class_fa=Admin().get_faculty_class(),st_id=Admin().get_max_studentid(),l_class=AdminUser().get_list_class_student(),l_faculty=AdminUser().get_list_faculty(),Message=mess)

@app.route('/delete_student',methods=['POST'])
def delete_student():
    """
    hàm xóa sinh viên 
    -input: studentID
    -return: message thông báo xóa thành công hay thất bại
    """
    studentid=request.form['studentid']
    try:
        Admin().delete_student(studentid)
        mess='success'
    except Exception as e:
        mess=f"Fail. {str(e)}"
    return render_template('student_record_manage.html',l_class_fa=Admin().get_faculty_class(),st_id=Admin().get_max_studentid(),l_class=AdminUser().get_list_class_student(),l_faculty=AdminUser().get_list_faculty(),Message=mess)

@app.route('/lecturer_record_manage')
def lecturer_record_manage():
    """
    hàm hướng đến lecturer_record_manage
    -input: none
    -return: page lecturer_record_manage.html 
    """
    return render_template('lecturer_record_manage.html',lt_id=Admin().get_max_lecturerid(),l_faculty=AdminUser().get_list_faculty())

@app.route('/search_lecturer_record',methods=['POST'])
def search_lecturer_record():
    """
    hàm search lecturer theo toàn bộ thông tin cá nhân, tìm kiếm gần đúng
    -input: 1 hoặc nhiều thông tin cá nhân
    -return: page lecturer_record_manage và danh sách giảng viên thỏa điều kiện
    """
    if request.method == 'POST':
        lecturer_id = request.form['lecturerid']
        lecturer_name = request.form['lecturerName']
        date_of_birth = request.form['dateOfBirth']
        gender = request.form['gender']
        address = request.form['address']
        email = request.form['email']
        phone_number = request.form['phoneNumber']
        selected_faculty = request.form['faculty']
        lt_list =Admin().search_lecturer(lecturer_id, lecturer_name, date_of_birth, gender, address, email, phone_number, selected_faculty)
        return render_template('lecturer_record_manage.html',lt_list=lt_list,lt_id=Admin().get_max_lecturerid(),l_faculty=AdminUser().get_list_faculty())


@app.route('/input_lecturer',methods=['POST'])
def input_lecturer():
    """
    hàm thêm giảng viên mới
    -input: thông tin cá nhân giảng viên
    -return: message thông báo thêm thành công hay thất bại
    """
    lecturerid=request.form['lecturerid']
    name=request.form['name']
    dob=request.form['dob']
    gender=request.form['gender']
    mail=request.form['email']
    facultyid=request.form['faculty']
    try:
        Admin().insert_lecturer(lecturerID=lecturerid,name=name,dateOfBirth=dob,gender=gender,email=mail,facultyID=facultyid)
        try:
            Admin().create_account(lecturerid,mail) ### mail từ request         
            mess='success. Account have been sended to user.'
        except Exception as e:
            mess=f'Fail. {str(e)}'
    except Exception as e:
        mess=f"Fail. {str(e)}"        
    return render_template('lecturer_record_manage.html',lt_id=Admin().get_max_lecturerid(),l_faculty=AdminUser().get_list_faculty(),Message=mess)

@app.route('/delete_lecturer',methods=['POST'])
def delete_lecturer():
    """
    hàm xóa giảng viên 
    -input: lecturerID
    -return: message thông báo xóa thành công hay thất bại
    """
    lecturerid=request.form['lecturerid']
    try:
        Admin().delete_lecturer(lecturerid)
        mess='success'
    except Exception as e:
        mess=f"Fail. {str(e)}"
    return render_template('lecturer_record_manage.html',lt_id=Admin().get_max_lecturerid(),l_faculty=AdminUser().get_list_faculty(),Message=mess)

@app.route('/course_manage')
def course_manage():
    """
    hàm hướng đến course_manage
    -input: none
    -return: page course_manage.html 
    """
    return render_template('course_manage.html',l_faculty=AdminUser().get_list_faculty(),l_course_full=Course().get_course())

@app.route('/search_course',methods=['POST'])
def search_course():
    """
    hàm search course theo toàn bộ thông tin, tìm kiếm gần đúng
    -input: 1 hoặc nhiều thông tin 
    -return: page course_manage và danh sách  course thỏa điều kiện
    """
    courseid=request.form['course_id']
    coursename=request.form['course_name']
    facultyid=request.form['faculty_id']
    return render_template('course_manage.html',l_course=Admin().search_course(courseid,coursename,facultyid),l_faculty=AdminUser().get_list_faculty(),l_course_full=Course().get_course()) 

@app.route('/add_course',methods=['POST'])
def add_course():
    """
    hàm thêm môn học mới
    -input: thông tin môn học
    -return: page course_manage và message báo thành công hay thất bại
    """
    courseid=request.form['course_id']
    coursename=request.form['course_name']
    facultyid=request.form['faculty_id']
    credit=request.form['credit']
    description=request.form['description']
    previous=request.form['previous_course']
    following=request.form['following_course']
    try:
        Admin().add_course(courseid=courseid,coursename=coursename,facultyid=facultyid,credit=credit,description=description,previous=previous,following=following)
        mess='Success'
    except Exception as e:
        mess=f"fail: {str(e)}"
    return render_template('course_manage.html',Message=mess,l_faculty=AdminUser().get_list_faculty(),l_course_full=Course().get_course())

@app.route('/delete_course',methods=['POST'])
def delete_course():
    """
    hàm delete môn học
    -input: courseID
    -return: page course_manage và message báo xóa thành công hay thất bại
    """
    courseid=request.form['courseid']
    try:
        Admin().delete_course(courseid)
        mess='success'
    except Exception as e:
        mess=f"fail: {str(e)}"
    return render_template('course_manage.html',Message=mess,l_faculty=AdminUser().get_list_faculty(),l_course_full=Course().get_course())

@app.route('/back_up')
def back_up():
    """
    hàm hướng tới page back up
    -input: note
    -return: page back_up
    """
    return render_template('back_up.html')

@app.route('/backup_login',methods=['POST'])
def backup_login():
    """
    hàm backup
    -input: username, password
    -return: page course_manage và message báo thông tin đăng nhập đúng hay sai hay đã back up thành công
    """
    username=request.form['username']
    password=request.form['password']
    if  username=="adminadmin" and Login(username,password).login()==True:
        try:
            Admin().backup_to_file()
            Admin().send_file_mail('tpmbdhieuvanpham@gmail.com')
            mess='Back up successfully. File backup was sended to your email'
            return render_template('back_up.html',Message=mess)
        except Exception as e:
            mess=f"fail: {str(e)}"
            return render_template('back_up.html',Message=mess)
    else:
        mess='Wrong username or password'
        return render_template('back_up.html',Message=mess)
