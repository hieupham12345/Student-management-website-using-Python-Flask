CREATE database STUDENTMANAGEMENT;
USE STUDENTMANAGEMENT;
CREATE TABLE Student (
    studentID CHAR(8) PRIMARY KEY,
    name NVARCHAR(30) NOT NULL,
    dateOfBirth DATETIME NOT NULL,
    gender CHAR(1) NOT NULL,
    address NVARCHAR(100) NOT NULL,
    email NVARCHAR(50) NOT NULL,
    phoneNumber CHAR(10) NOT NULL,
    classID CHAR(8)
);
CREATE TABLE Lecturer (
  lecturerID CHAR(8) PRIMARY KEY,
  name NVARCHAR(30) NOT NULL,
  dateOfBirth DATETIME NOT NULL,
  gender CHAR(1) NOT NULL,
  address NVARCHAR(100) NOT NULL,
  email NVARCHAR(50) NOT NULL,
  phoneNumber CHAR(10) NOT NULL,
  facultyID CHAR(8) NOT NULL
);
CREATE TABLE AdminUser (
  staffID CHAR(8) PRIMARY KEY,
  name NVARCHAR(30) NOT NULL,
  dateOfBirth DATETIME NOT NULL,
  gender CHAR(1) NOT NULL,
  address NVARCHAR(100) NOT NULL,
  email NVARCHAR(50) NOT NULL,
  phoneNumber CHAR(10) NOT NULL,
  departmentID CHAR(8) NOT NULL
);
CREATE TABLE Course (
    courseID CHAR(8) PRIMARY KEY,
    courseName NVARCHAR(50) NOT NULL,
    facultyID CHAR(8) NOT NULL,
    credit INT NOT NULL,
    description text,
    previousCourse CHAR(8),
    followingCourse CHAR(8)
);
CREATE TABLE Grade (
  studentID CHAR(8) NOT NULL,
  courseID CHAR(8) NOT NULL,
  semester CHAR(16) NOT NULL,
  lecturerID CHAR(8) NOT NULL,
  process FLOAT NULL,
  mid float null,
  final float null,
  avg float null,
  PRIMARY KEY (studentID, courseID, semester),
  FOREIGN KEY (studentID) REFERENCES Student (studentID),
  FOREIGN KEY (courseID) REFERENCES Course (courseID),
  FOREIGN KEY (lecturerID) REFERENCES Lecturer (lecturerID)
);

CREATE TABLE Faculty (
    facultyID CHAR(8) PRIMARY KEY,
    facultyName NVARCHAR(100) NOT NULL,
    dean NVARCHAR(30) NOT NULL,
    numberOfLecturer INT  NULL,
    numberOfStudent INT  NULL
);
CREATE TABLE Classroom (
    classroomID CHAR(8) PRIMARY KEY
);
CREATE TABLE schedule (
  scheduleID varchar(8) NOT NULL,
  courseID CHAR(8) NOT NULL,
  day ENUM('mon', 'tue', 'wed', 'thu', 'fri') NOT NULL,
  time TIME NOT NULL,
  classroomID CHAR(8) NOT NULL,
  lecturerID char(8),
  semester char(15),
  PRIMARY KEY (scheduleID),
  foreign key (LECTURERID) REFERENCES LECTURER(LECTURERID),
  foreign key (courseid) references course(courseid),
  foreign key (classroomid) references classroom(classroomid)
);

CREATE TABLE student_schedule (
  studentID char(8),
  scheduleid varchar(8),
  primary key(studentid,scheduleid),
  foreign key (studentid) references student(studentid),
  foreign key (scheduleid) references schedule(scheduleid)
);
CREATE TABLE TestSchedule (
	scheduleID varchar(8),
    classroomID CHAR(8),
    Time DATETIME,
    CourseID CHAR(8),
    LecturerID Char(8),
    PRIMARY KEY (classroomID,time,scheduleid),
    FOREIGN KEY (CourseID) REFERENCES Course (courseID),
    FOREIGN KEY (classroomID) REFERENCES Classroom (classroomID),
    FOREIGN KEY (scheduleID) references schedule(scheduleid),
    FOREIGN KEY (lecturerID) references lecturer(lecturerid)
);
CREATE TABLE StudentClass (
    classID CHAR(8) PRIMARY KEY,
    academicYear YEAR NOT NULL,
    numberOfStudent INT  NULL,
    lecturerID CHAR(8) NOT NULL,
    FOREIGN KEY (lecturerID) REFERENCES Lecturer(lecturerID)
);
CREATE TABLE Faculty_class(
	facultyID char(8),
    classID char(8),
    primary key (facultyid, classid),
    foreign key (facultyid) references faculty(facultyid),
    foreign key (classid) references studentclass(classid)
);
CREATE TABLE TuitionFee (
  TuitionFee NUMERIC,
  Status NVARCHAR(20),
  StudentID CHAR(8),
  sumcredit int,
  primary key (STUDENTID,TUITIONFEE),
  FOREIGN KEY (StudentID) REFERENCES Student (StudentID)
);

CREATE TABLE Course_register (
	studentID char(8),
    courseID CHAR(8),
    semester char(8),
    primary key(studentid, courseid),
    foreign key(studentid) references student(studentid),
    foreign key(courseid) references course(courseid)
);
CREATE TABLE Account (
   username VARCHAR(50) NOT NULL,
   password VARCHAR(256) NOT NULL,
   PRIMARY KEY (username)
);
ALTER TABLE STUDENT
ADD CONSTRAINT FK1 FOREIGN KEY (classID) REFERENCES StudentClass (classID);

ALTER TABLE LECTURER
ADD CONSTRAINT FK3 FOREIGN KEY (FACULTYID) REFERENCES FACULTY (FACULTYID);

ALTER TABLE COURSE
ADD CONSTRAINT FK5 FOREIGN KEY (FACULTYID) REFERENCES FACULTY (FACULTYID);

CREATE TABLE attendance(
	scheduleid varchar(8),
	status varchar(8) NOT NULL,
    FOREIGN KEY (SCHEDULEID) REFERENCES SCHEDULE(SCHEDULEID)
);
INSERT INTO attendance (scheduleid, status)
SELECT SCHEDULEID, 'close' AS status
FROM SCHEDULE;

CREATE TABLE attendance_add(
	studentid char(8),
    scheduleid char(8),
    time datetime,
    note text,
    primary key(studentid,scheduleid),
    foreign key (studentid) references student(studentid),
	foreign key (scheduleid) references schedule(scheduleid)
);


DELIMITER //
CREATE TRIGGER insert_attendance_trigger
AFTER INSERT ON schedule
FOR EACH ROW
BEGIN
    INSERT INTO attendance (scheduleid, status)
    VALUES (NEW.scheduleid, 'close');
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_numberOfLecturer
AFTER INSERT ON Lecturer
FOR EACH ROW
BEGIN
    UPDATE Faculty
    SET numberOfLecturer = (
        SELECT COUNT(lecturerID)
        FROM Lecturer
        WHERE facultyID = NEW.facultyID
        GROUP BY facultyID
    )
    WHERE facultyID = NEW.facultyID;
END //
DELIMITER ;

#cần trigger auto update
DELIMITER //
CREATE TRIGGER update_numberOfStudent
AFTER INSERT ON Student
FOR EACH ROW
BEGIN
    UPDATE StudentClass
    SET numberOfStudent = (
        SELECT COUNT(studentID)
        FROM Student
        WHERE classID = NEW.classID
        GROUP BY classID
    )
    WHERE classID = NEW.classID;
END //
DELIMITER ;
DELIMITER //
CREATE TRIGGER update_numberOfStudent_1
AFTER update ON studentclass
FOR EACH ROW
BEGIN
    UPDATE faculty as E
    SET numberOfStudent = (
        SELECT sum(numberofstudent)
        FROM studentclass inner join faculty_class on studentclass.classid=faculty_class.classid
        GROUP BY facultyid
        having facultyid=E.facultyid
    );
END //
DELIMITER ;
DELIMITER //
CREATE TRIGGER check_grade_range
BEFORE INSERT ON Grade
FOR EACH ROW
BEGIN
    IF NEW.process < 0 OR NEW.process > 10 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid process grade';
    END IF;
    
    IF NEW.mid < 0 OR NEW.mid > 10 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid mid grade';
    END IF;
    
    IF NEW.final < 0 OR NEW.final > 10 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid final grade';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER check_grade_range_update
BEFORE UPDATE ON Grade
FOR EACH ROW
BEGIN
    IF NEW.process < 0 OR NEW.process > 10 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid process grade';
    END IF;
    
    IF NEW.mid < 0 OR NEW.mid > 10 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid mid grade';
    END IF;
    
    IF NEW.final < 0 OR NEW.final > 10 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid final grade';
    END IF;
END //
DELIMITER ;

INSERT INTO Grade (studentID, courseID, semester, lecturerID, process, mid, final,avg)
VALUES 
('ST000011', 'IT100', '2021.1', 'LT000001', 8.5, 6.75, 12,NULL);
delete from grade where studentid='st000011' and courseid='it100';

DELIMITER //
CREATE TRIGGER insert_course_register
AFTER INSERT ON course_register
FOR EACH ROW
BEGIN
	IF EXISTS (SELECT * FROM TUITIONFEE WHERE STUDENTID=NEW.STUDENTID) THEN
		UPDATE TUITIONFEE
        SET TUITIONFEE=TUITIONFEE+400000*(SELECT CREDIT FROM COURSE WHERE COURSEID=NEW.COURSEID), sumcredit=sumcredit+(SELECT CREDIT FROM COURSE WHERE COURSEID=NEW.COURSEID)
        WHERE STUDENTID=NEW.STUDENTID;
    ELSE
		INSERT INTO TuitionFee (TuitionFee, Status, StudentID, sumcredit)
		SELECT 400000*(SELECT CREDIT FROM COURSE WHERE COURSEID=NEW.COURSEID), 'unpaid',NEW.STUDENTID, (SELECT CREDIT FROM COURSE WHERE COURSEID=NEW.COURSEID)
		FROM course_register
		INNER JOIN Course ON course_register.CourseID = Course.CourseID;
	END IF;
END//
DELIMITER;

DELIMITER //
CREATE TRIGGER delete_course_register
AFTER DELETE ON course_register
FOR EACH ROW
BEGIN
		UPDATE TUITIONFEE
        SET TUITIONFEE=TUITIONFEE-400000*(SELECT CREDIT FROM COURSE WHERE COURSEID=old.COURSEID),sumcredit=sumcredit-(SELECT CREDIT FROM COURSE WHERE COURSEID=old.COURSEID)
        WHERE STUDENTID=old.STUDENTID;
END //
DEMILITER;

DELIMITER //
CREATE TRIGGER check_previous_course
BEFORE INSERT ON course_register
FOR EACH ROW
BEGIN
    DECLARE previous_course INT;
    SET previous_course = (
        SELECT distinct previouscourse
        FROM course
		WHERE course.courseid = new.courseid
    );
    IF previous_course not in (select courseid from grade where studentid=new.studentid) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Lỗi môn học trước';
    END IF;
END //
DELIMITER ;
drop trigger check_previous_course;