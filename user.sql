-- USER for STUDENT
CREATE USER 'student'@'localhost' IDENTIFIED BY 'password'; 

GRANT UPDATE ON studentmanagement.student TO 'student'@'localhost';
GRANT SELECT ON studentmanagement.* TO 'student'@'localhost';
GRANT INSERT ON studentmanagement.course_register to 'student'@'localhost';
GRANT DELETE ON studentmanagement.course_register to 'student'@'localhost';
GRANT INSERT, UPDATE ON studentmanagement.attendance_add to 'student'@'localhost';


-- USER for LECTURER
CREATE USER 'lecturer'@'localhost' IDENTIFIED BY 'password';

GRANT SELECT ON STUDENTMANAGEMENT.* TO 'lecturer'@'LOCALHOST';
GRANT UPDATE ON studentmanagement.lecturer TO 'lecturer'@'LOCALHOST';
GRANT INSERT ON studentmanagement.GRADE TO 'lecturer'@'LOCALHOST';
GRANT UPDATE ON studentmanagement.GRADE TO 'lecturer'@'LOCALHOST';
GRANT UPDATE ON studentmanagement.attendance TO 'lecturer'@'localhost';
GRANT INSERT, UPDATE,DELETE ON studentmanagement.attendance_add to 'lecturer'@'localhost';


-- USER for userADMIN 
CREATE USER 'admin'@'localhost' identified BY 'admin';

GRANT SELECT ON studentmanagement.* TO 'admin'@'localhost';
GRANT UPDATE,INSERT,DELETE ON studentmanagement.schedule to 'admin'@'localhost';
GRANT UPDATE,INSERT,DELETE ON studentmanagement.student_schedule to 'admin'@'localhost';
GRANT UPDATE,INSERT,DELETE ON studentmanagement.testschedule to 'admin'@'localhost';
GRANT UPDATE ON studentmanagement.account to 'admin'@'localhost';

-- USER FOR ADMIN
CREATE USER 'adminadmin'@'localhost' identified by 'admin';

GRANT UPDATE, INSERT, DELETE ON studentmanagement.student to 'adminadmin'@'localhost';
GRANT UPDATE, INSERT, DELETE ON studentmanagement.lecturer to 'adminadmin'@'localhost';
GRANT UPDATE, INSERT, DELETE ON studentmanagement.adminuser to 'adminadmin'@'localhost';
GRANT UPDATE, INSERT, DELETE ON studentmanagement.account to 'adminadmin'@'localhost';
GRANT SELECT ON studentmanagement.* TO 'adminadmin'@'localhost';
GRANT INSERT, UPDATE,DELETE ON studentmanagement.course to 'adminadmin'@'localhost';
GRANT SELECT, SHOW VIEW, EVENT, TRIGGER, LOCK TABLES, RELOAD ON *.* TO 'adminadmin'@'localhost';



show grants for  'lecturer'@'localhost';