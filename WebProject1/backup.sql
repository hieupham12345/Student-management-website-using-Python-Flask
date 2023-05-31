CREATE DATABASE IF NOT EXISTS database_name;
USE database_name;
CREATE TABLE `account` (
  `username` varchar(50) NOT NULL,
  `password` varchar(256) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO account VALUES ('ad000001', '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e');
INSERT INTO account VALUES ('adminadmin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9');
INSERT INTO account VALUES ('lt000001', '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e');
INSERT INTO account VALUES ('st000001', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
CREATE TABLE `adminuser` (
  `staffID` char(8) NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `dateOfBirth` datetime NOT NULL,
  `gender` char(1) NOT NULL,
  `address` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `phoneNumber` char(10) NOT NULL,
  `departmentID` char(8) NOT NULL,
  PRIMARY KEY (`staffID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO adminuser VALUES ('AD000001', 'Nguyễn Văn A', '1980-01-01 00:00:00', 'M', 'Số 10, Đường 3/2, Quận 10, TP. Hồ Chí Minh', 'nguyenvana@gmail.com', '0901234567', 'DPT001');
INSERT INTO adminuser VALUES ('AD000002', 'Trần Thị B', '1985-05-15 00:00:00', 'F', 'Số 20, Đường Lê Văn Việt, Quận 9, TP. Hồ Chí Minh', 'tranthib@gmail.com', '0902345678', 'DPT002');
INSERT INTO adminuser VALUES ('AD000003', 'Phạm Thành C', '1990-10-20 00:00:00', 'M', 'Số 30, Đường Phan Đăng Lưu, Quận Phú Nhuận, TP. Hồ Chí Minh', 'phamthanhc@gmail.com', '0903456789', 'DPT003');
INSERT INTO adminuser VALUES ('AD000004', 'Lê Thị D', '1982-06-05 00:00:00', 'F', 'Số 40, Đường Trần Quang Khải, Quận 1, TP. Hồ Chí Minh', 'lethid@gmail.com', '0904567890', 'DPT004');
INSERT INTO adminuser VALUES ('AD000005', 'Hoàng Thanh E', '1987-03-10 00:00:00', 'M', 'Số 50, Đường Trần Hưng Đạo, Quận 5, TP. Hồ Chí Minh', 'hoangthanhe@gmail.com', '0905678901', 'DPT005');
CREATE TABLE `attendance` (
  `scheduleid` varchar(8) DEFAULT NULL,
  `status` varchar(8) NOT NULL,
  KEY `scheduleid` (`scheduleid`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`scheduleid`) REFERENCES `schedule` (`scheduleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO attendance VALUES ('SC6', 'close');
INSERT INTO attendance VALUES ('SC7', 'close');
INSERT INTO attendance VALUES ('SC8', 'close');
INSERT INTO attendance VALUES ('SC9', 'close');
INSERT INTO attendance VALUES ('SC10', 'close');
CREATE TABLE `attendance_add` (
  `studentid` char(8) NOT NULL,
  `scheduleid` char(8) NOT NULL,
  `time` datetime DEFAULT NULL,
  `note` text,
  PRIMARY KEY (`studentid`,`scheduleid`),
  KEY `scheduleid` (`scheduleid`),
  CONSTRAINT `attendance_add_ibfk_1` FOREIGN KEY (`studentid`) REFERENCES `student` (`studentID`),
  CONSTRAINT `attendance_add_ibfk_2` FOREIGN KEY (`scheduleid`) REFERENCES `schedule` (`scheduleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `classroom` (
  `classroomID` char(8) NOT NULL,
  PRIMARY KEY (`classroomID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO classroom VALUES ('C001');
INSERT INTO classroom VALUES ('C002');
INSERT INTO classroom VALUES ('C003');
INSERT INTO classroom VALUES ('C004');
INSERT INTO classroom VALUES ('C005');
INSERT INTO classroom VALUES ('C006');
INSERT INTO classroom VALUES ('C007');
INSERT INTO classroom VALUES ('C008');
INSERT INTO classroom VALUES ('C009');
INSERT INTO classroom VALUES ('C010');
INSERT INTO classroom VALUES ('C011');
INSERT INTO classroom VALUES ('C012');
INSERT INTO classroom VALUES ('C013');
INSERT INTO classroom VALUES ('C014');
INSERT INTO classroom VALUES ('C015');
INSERT INTO classroom VALUES ('C016');
INSERT INTO classroom VALUES ('C017');
INSERT INTO classroom VALUES ('C018');
INSERT INTO classroom VALUES ('C019');
INSERT INTO classroom VALUES ('C020');
CREATE TABLE `course` (
  `courseID` char(8) NOT NULL,
  `courseName` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `facultyID` char(8) NOT NULL,
  `credit` int NOT NULL,
  `description` text,
  `previousCourse` char(8) DEFAULT NULL,
  `followingCourse` char(8) DEFAULT NULL,
  PRIMARY KEY (`courseID`),
  KEY `FK5` (`facultyID`),
  CONSTRAINT `FK5` FOREIGN KEY (`facultyID`) REFERENCES `faculty` (`facultyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO course VALUES ('CN100', 'Giới thiệu về Mạng máy tính', 'ITD03', '3', 'Khóa học này cung cấp một giới thiệu về mạng máy tính.', 'None', 'CN101');
INSERT INTO course VALUES ('CN101', 'Các giao thức mạng', 'ITD03', '3', 'Khóa học này bao gồm các nguyên tắc và thực hành của các giao thức mạng.', 'None', 'CN102');
INSERT INTO course VALUES ('CN102', 'Bảo mật mạng', 'ITD03', '3', 'Khóa học này bao gồm các nguyên tắc và thực hành của bảo mật mạng.', 'None', 'CN103');
INSERT INTO course VALUES ('CN103', 'Thiết kế mạng', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về thiết kế mạng.', 'None', 'CN104');
INSERT INTO course VALUES ('CN104', 'Quản trị mạng', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về quản trị mạng.', 'None', 'CN105');
INSERT INTO course VALUES ('CN105', 'Mạng không dây', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về mạng không dây.', 'CN101', 'CN106');
INSERT INTO course VALUES ('CN106', 'Mạng viễn thông', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về mạng viễn thông.', 'CN102', 'CN107');
INSERT INTO course VALUES ('CN107', 'Mạng di động', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về mạng di động.', 'CN102', 'CN108');
INSERT INTO course VALUES ('CN108', 'Mạng máy tính công nghiệp', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về mạng máy tính công nghiệp.', 'CN103', 'CN109');
INSERT INTO course VALUES ('CN109', 'Mạng máy tính vô tuyến', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về mạng máy tính vô tuyến.', 'CN104', 'CN110');
INSERT INTO course VALUES ('CN110', 'Mạng máy tính cá nhân', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về mạng máy tính cá nhân.', 'CN109', 'CN111');
INSERT INTO course VALUES ('CN111', 'Mạng máy tính doanh nghiệp', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về mạng máy tính doanh nghiệp.', 'CN108', 'CN112');
INSERT INTO course VALUES ('CN112', 'Mạng máy tính truyền thông', 'ITD03', '3', 'Khóa học này cung cấp kiến thức về mạng máy tính truyền thông.', 'CN101', 'None');
INSERT INTO course VALUES ('CS101', 'Lập trình căn bản', 'ITD02', '3', 'Học về cú pháp, kiến thức căn bản và logic lập trình.', 'None', 'CS102');
INSERT INTO course VALUES ('CS102', 'Cấu trúc dữ liệu và giải thuật', 'ITD02', '4', 'Nắm vững các cấu trúc dữ liệu và thuật toán để giải quyết các vấn đề phức tạp.', 'None', 'CS103');
INSERT INTO course VALUES ('CS103', 'Hệ điều hành', 'ITD02', '3', 'Tìm hiểu về nguyên lý hoạt động của hệ điều hành và quản lý tài nguyên hệ thống.', 'None', 'CS104');
INSERT INTO course VALUES ('CS104', 'Cơ sở dữ liệu', 'ITD02', '4', 'Học về thiết kế, triển khai và quản lý cơ sở dữ liệu.', 'None', 'CS105');
INSERT INTO course VALUES ('CS105', 'Mạng máy tính', 'ITD02', '3', 'Tìm hiểu về mạng máy tính, giao thức truyền thông và quản lý mạng.', 'None', 'CS106');
INSERT INTO course VALUES ('CS106', 'Ngôn ngữ lập trình nâng cao', 'ITD02', '3', 'Nghiên cứu các ngôn ngữ lập trình phức tạp hơn như Java, C++, Python.', 'CS100', 'CS107');
INSERT INTO course VALUES ('CS107', 'Trực quan hóa dữ liệu', 'ITD02', '3', 'Học cách biểu diễn dữ liệu một cách trực quan thông qua đồ họa và các công cụ tương tự.', 'CS101', 'CS108');
INSERT INTO course VALUES ('CS108', 'Trí tuệ nhân tạo', 'ITD02', '4', 'Tìm hiểu về các thuật toán và kỹ thuật trong lĩnh vực trí tuệ nhân tạo như học máy và thị giác máy tính.', 'CS102', 'CS109');
INSERT INTO course VALUES ('CS109', 'Xử lý ngôn ngữ tự nhiên', 'ITD02', '3', 'Học cách xử lý và hiểu ngôn ngữ tự nhiên bằng các phương pháp và thuật toán.', 'CS104', 'CS110');
INSERT INTO course VALUES ('CS110', 'An toàn thông tin', 'ITD02', '3', 'Tìm hiểu về các phương pháp bảo mật và quản lý rủi ro thông tin.', 'CS105', 'CS111');
INSERT INTO course VALUES ('CS111', 'Đồ họa máy tính', 'ITD02', '4', 'Nghiên cứu về đồ họa máy tính, thiết kế giao diện người dùng và thị giác máy tính.', 'CS110', 'CS112');
INSERT INTO course VALUES ('CS112', 'Công nghệ web', 'ITD02', '3', 'Học về phát triển ứng dụng web, các ngôn ngữ lập trình web như HTML, CSS, JavaScript và các framework như React, Angular, Django.', 'CS101', 'CS113');
INSERT INTO course VALUES ('CS113', 'Công nghệ di động', 'ITD02', '3', 'Tìm hiểu về phát triển ứng dụng di động trên các nền tảng như Android và iOS.', 'CS102', 'CS114');
INSERT INTO course VALUES ('CS114', 'Khai phá dữ liệu', 'ITD02', '4', 'Nghiên cứu về các kỹ thuật khai phá dữ liệu để tìm hiểu thông tin tiềm ẩn và mô hình dữ liệu.', 'CS105', 'CS115');
INSERT INTO course VALUES ('CS115', 'Quản lý dự án phần mềm', 'ITD02', '3', 'Học về quy trình phát triển phần mềm, quản lý dự án và công cụ hỗ trợ quản lý.', 'CS114', 'None');
INSERT INTO course VALUES ('DC100', 'Cơ sở dữ liệu', 'ITD04', '3', 'Nền tảng về cách tổ chức, quản lý và truy xuất dữ liệu.', 'None', 'DC101');
INSERT INTO course VALUES ('DC101', 'Xử lý dữ liệu', 'ITD04', '3', 'Phân tích và biến đổi dữ liệu để chuẩn bị cho quá trình phân tích dữ liệu.', 'None', 'DC102');
INSERT INTO course VALUES ('DC102', 'Thống kê', 'ITD04', '3', 'Áp dụng các phương pháp thống kê để phân tích dữ liệu và rút ra kết luận.', 'None', 'DC103');
INSERT INTO course VALUES ('DC103', 'Học máy', 'ITD04', '3', 'Nghiên cứu cách xây dựng mô hình dự đoán và phân loại dữ liệu.', 'None', 'DC104');
INSERT INTO course VALUES ('DC104', 'Khai phá dữ liệu', 'ITD04', '3', 'Tìm hiểu các phương pháp để khám phá tri thức và thông tin tiềm ẩn trong dữ liệu.', 'None', 'DC105');
INSERT INTO course VALUES ('DC105', 'Xử lý ngôn ngữ tự nhiên', 'ITD04', '3', 'Nghiên cứu về cách xử lý và hiểu ngôn ngữ tự nhiên bằng các thuật toán máy học.', 'DC104', 'DC106');
INSERT INTO course VALUES ('DC106', 'Trí tuệ nhân tạo', 'ITD04', '3', 'Nghiên cứu về cách xây dựng các hệ thống thông minh và học máy có khả năng tự học.', 'DC104', 'DC107');
INSERT INTO course VALUES ('DC107', 'Mạng neuron', 'ITD04', '3', 'Nghiên cứu về cách xây dựng và huấn luyện mạng neuron nhân tạo.', 'DC102', 'DC108');
INSERT INTO course VALUES ('DC108', 'Khám phá dữ liệu', 'ITD04', '3', 'Áp dụng các phương pháp khám phá dữ liệu để tìm ra thông tin hữu ích.', 'DC103', 'DC109');
INSERT INTO course VALUES ('DC109', 'Khai thác dữ liệu', 'ITD04', '3', 'Xác định và trích xuất tri thức từ dữ liệu có cấu trúc và không có cấu trúc.', 'DC101', 'DC110');
INSERT INTO course VALUES ('DC110', 'Đại số tuyến tính', 'ITD04', '3', 'Nghiên cứu về các phép toán và ánh xạ tuyến tính để phân tích dữ liệu.', 'DC109', 'DC111');
INSERT INTO course VALUES ('DC111', 'Lập trình Python', 'ITD04', '3', 'Học ngôn ngữ lập trình phổ biến trong khoa học dữ liệu và machine learning.', 'DC109', 'DC112');
INSERT INTO course VALUES ('DC112', 'Visual Analytics', 'ITD04', '3', 'Khám phá và biểu đồ hóa dữ liệu để hiểu thông tin từ dữ liệu.', 'DC108', 'DC113');
INSERT INTO course VALUES ('DC113', 'Data Mining', 'ITD04', '3', 'Sử dụng các phương pháp và thuật toán để khai thác tri thức từ dữ liệu lớn.', 'DC102', 'DC114');
INSERT INTO course VALUES ('DC114', 'Big Data Analytics', 'ITD04', '3', 'Nghiên cứu về cách xử lý và phân tích dữ liệu lớn để tìm ra thông tin quan trọng và xu hướng.', 'DC113', 'None');
INSERT INTO course VALUES ('IT100', 'Cấu trúc dữ liệu và giải thuật', 'ITD01', '3', 'None', 'None', 'IT101');
INSERT INTO course VALUES ('IT101', 'Lập trình C/C++', 'ITD01', '4', 'None', 'None', 'IT102');
INSERT INTO course VALUES ('IT102', 'Lập trình Java', 'ITD01', '4', 'None', 'None', 'IT103');
INSERT INTO course VALUES ('IT103', 'Lập trình Python', 'ITD01', '3', 'None', 'None', 'IT104');
INSERT INTO course VALUES ('IT104', 'Hệ điều hành', 'ITD01', '3', 'None', 'None', 'IT105');
INSERT INTO course VALUES ('IT105', 'Mạng máy tính', 'ITD01', '3', 'None', 'IT102', 'IT106');
INSERT INTO course VALUES ('IT106', 'Cơ sở dữ liệu', 'ITD01', '3', 'None', 'IT101', 'IT107');
INSERT INTO course VALUES ('IT107', 'Quản lý dự án phần mềm', 'ITD01', '3', 'None', 'IT103', 'IT108');
INSERT INTO course VALUES ('IT108', 'Hệ thống thông tin', 'ITD01', '3', 'None', 'IT105', 'IT109');
INSERT INTO course VALUES ('IT109', 'An toàn thông tin', 'ITD01', '3', 'None', 'IT104', 'IT110');
INSERT INTO course VALUES ('IT110', 'Kỹ thuật truyền thông', 'ITD01', '3', 'None', 'IT109', 'IT111');
INSERT INTO course VALUES ('IT111', 'Trí tuệ nhân tạo', 'ITD01', '3', 'None', 'IT107', 'IT112');
INSERT INTO course VALUES ('IT112', 'Thiết kế giao diện người dùng', 'ITD01', '3', 'None', 'IT101', 'IT113');
INSERT INTO course VALUES ('IT113', 'Phân tích và thiết kế hệ thống thông tin', 'ITD01', '3', 'None', 'IT102', 'IT114');
INSERT INTO course VALUES ('IT114', 'Lập trình web', 'ITD01', '3', 'None', 'IT113', 'IT107');
INSERT INTO course VALUES ('IT115', 'Học máy (Machine Learning)', 'ITD01', '3', 'None', 'IT104', 'IT116');
INSERT INTO course VALUES ('IT116', 'Phân tích dữ liệu (Data Analytics)', 'ITD01', '3', 'None', 'IT105', 'IT117');
INSERT INTO course VALUES ('IT117', 'Mạng xã hội và phân tích mạng xã hội', 'ITD01', '3', 'None', 'IT106', 'IT118');
INSERT INTO course VALUES ('IT118', 'Kỹ thuật phần mềm', 'ITD01', '3', 'None', 'IT107', 'IT119');
INSERT INTO course VALUES ('IT119', 'Đồ án tốt nghiệp', 'ITD01', '4', 'None', 'IT108', 'None');
CREATE TABLE `course_register` (
  `studentID` char(8) NOT NULL,
  `courseID` char(8) NOT NULL,
  `semester` char(8) DEFAULT NULL,
  PRIMARY KEY (`studentID`,`courseID`),
  KEY `courseID` (`courseID`),
  CONSTRAINT `course_register_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `student` (`studentID`),
  CONSTRAINT `course_register_ibfk_2` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO course_register VALUES ('st000001', 'CN100', 'None');
INSERT INTO course_register VALUES ('st000001', 'CN101', 'None');
INSERT INTO course_register VALUES ('st000001', 'IT119', 'None');
CREATE TABLE `faculty` (
  `facultyID` char(8) NOT NULL,
  `facultyName` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `dean` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `numberOfLecturer` int DEFAULT NULL,
  `numberOfStudent` int DEFAULT NULL,
  PRIMARY KEY (`facultyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO faculty VALUES ('ITD01', 'Khoa Công nghệ thông tin ', 'Nguyễn Văn A', '13', '47');
INSERT INTO faculty VALUES ('ITD02', 'Khoa học máy tính', 'Trần Thị B', '3', 'None');
INSERT INTO faculty VALUES ('ITD03', 'Mạng máy tính và Truyền thông', 'Lê Văn C', '6', 'None');
INSERT INTO faculty VALUES ('ITD04', 'Khoa học dữ liệu', 'Phạm Thị D', '4', 'None');
CREATE TABLE `faculty_class` (
  `facultyID` char(8) NOT NULL,
  `classID` char(8) NOT NULL,
  PRIMARY KEY (`facultyID`,`classID`),
  KEY `classID` (`classID`),
  CONSTRAINT `faculty_class_ibfk_1` FOREIGN KEY (`facultyID`) REFERENCES `faculty` (`facultyID`),
  CONSTRAINT `faculty_class_ibfk_2` FOREIGN KEY (`classID`) REFERENCES `studentclass` (`classID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO faculty_class VALUES ('ITD01', 'CNTT2020');
INSERT INTO faculty_class VALUES ('ITD01', 'CNTT2021');
INSERT INTO faculty_class VALUES ('ITD02', 'KHMT2020');
INSERT INTO faculty_class VALUES ('ITD02', 'KHMT2021');
INSERT INTO faculty_class VALUES ('ITD03', 'MMT2021');
CREATE TABLE `grade` (
  `studentID` char(8) NOT NULL,
  `courseID` char(8) NOT NULL,
  `semester` char(16) NOT NULL,
  `lecturerID` char(8) NOT NULL,
  `process` float DEFAULT NULL,
  `mid` float DEFAULT NULL,
  `final` float DEFAULT NULL,
  `avg` float DEFAULT NULL,
  PRIMARY KEY (`studentID`,`courseID`,`semester`),
  KEY `courseID` (`courseID`),
  KEY `lecturerID` (`lecturerID`),
  CONSTRAINT `grade_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `student` (`studentID`),
  CONSTRAINT `grade_ibfk_2` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`),
  CONSTRAINT `grade_ibfk_3` FOREIGN KEY (`lecturerID`) REFERENCES `lecturer` (`lecturerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO grade VALUES ('ST000001', 'IT100', '2021.1', 'LT000001', '8.5', '6.75', '9.25', '8.35');
INSERT INTO grade VALUES ('ST000001', 'IT101', '2021.1', 'LT000002', '4.25', '7.5', '8.0', '7.1');
INSERT INTO grade VALUES ('ST000001', 'IT102', '2021.1', 'LT000003', '9.0', '3.25', '5.5', '5.525');
INSERT INTO grade VALUES ('ST000001', 'IT103', '2021.1', 'LT000001', '6.75', '8.25', '7.0', '7.325');
INSERT INTO grade VALUES ('ST000001', 'IT104', '2021.1', 'LT000002', '3.5', '4.75', '6.25', '5.25');
INSERT INTO grade VALUES ('ST000001', 'IT105', '2021.2', 'LT000002', '4.25', '7.5', '8.0', '7.1');
INSERT INTO grade VALUES ('ST000001', 'IT106', '2021.2', 'LT000013', '9.0', '3.25', '5.5', '5.525');
INSERT INTO grade VALUES ('ST000001', 'IT107', '2021.2', 'LT000020', '6.75', '8.25', '7.0', '7.325');
INSERT INTO grade VALUES ('ST000001', 'IT108', '2021.2', 'LT000021', '3.5', '4.75', '6.25', '5.25');
INSERT INTO grade VALUES ('ST000001', 'IT109', '2021.2', 'LT000021', '6.5', '5.75', '6.25', '6.15');
INSERT INTO grade VALUES ('ST000001', 'IT110', '2022.1', 'LT000023', '5.75', '6.5', '7.75', '6.975');
INSERT INTO grade VALUES ('ST000001', 'IT111', '2022.1', 'LT000024', '8.0', '7.25', '9.0', '8.275');
INSERT INTO grade VALUES ('ST000001', 'IT112', '2022.1', 'LT000025', '6.25', '5.5', '8.0', '6.9');
INSERT INTO grade VALUES ('ST000001', 'IT113', '2022.1', 'LT000026', '4.75', '6.75', '7.5', '6.725');
INSERT INTO grade VALUES ('ST000001', 'IT114', '2022.1', 'LT000027', '9.25', '8.0', '9.75', '9.125');
INSERT INTO grade VALUES ('ST000001', 'IT115', '2022.2', 'LT000028', '7.0', '7.75', '6.5', '6.975');
INSERT INTO grade VALUES ('ST000001', 'IT116', '2022.2', 'LT000029', '5.5', '4.25', '6.75', '5.75');
INSERT INTO grade VALUES ('ST000001', 'IT117', '2022.2', 'LT000020', '8.25', '9.0', '7.5', '8.1');
INSERT INTO grade VALUES ('ST000001', 'IT118', '2022.2', 'LT000021', '6.5', '8.5', '9.0', '8.35');
CREATE TABLE `lecturer` (
  `lecturerID` char(8) NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `dateOfBirth` datetime NOT NULL,
  `gender` char(1) NOT NULL,
  `address` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `phoneNumber` char(10) NOT NULL,
  `facultyID` char(8) NOT NULL,
  PRIMARY KEY (`lecturerID`),
  KEY `FK3` (`facultyID`),
  CONSTRAINT `FK3` FOREIGN KEY (`facultyID`) REFERENCES `faculty` (`facultyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO lecturer VALUES ('LT000001', 'Nguyen Van X', '1990-01-01 00:00:00', 'M', '123 Nguyen Van Cu, Quan 5, TP. Ho Chi Minh', 'nx@itd.edu.vn', '0123456789', 'ITD01');
INSERT INTO lecturer VALUES ('LT000002', 'Tran Thi Y', '1985-02-10 00:00:00', 'F', '456 Le Van Sy, Quan 3, TP. Ho Chi Minh', 'ty@itd.edu.vn', '0987654321', 'ITD01');
INSERT INTO lecturer VALUES ('LT000003', 'Pham Van Z', '1977-07-15 00:00:00', 'M', '789 Pham Van Dong, Quan 12, TP. Ho Chi Minh', 'pz@itd.edu.vn', '0111222333', 'ITD02');
INSERT INTO lecturer VALUES ('LT000004', 'Hoang Thi T', '1989-06-20 00:00:00', 'F', '321 Nguyen Tri Phuong, Quan 10, TP. Ho Chi Minh', 'ht@itd.edu.vn', '0333444555', 'ITD02');
INSERT INTO lecturer VALUES ('LT000005', 'Le Van U', '1980-12-31 00:00:00', 'M', '555 Ly Thuong Kiet, Quan 10, TP. Ho Chi Minh', 'lvu@itd.edu.vn', '0123456789', 'ITD03');
INSERT INTO lecturer VALUES ('LT000006', 'Nguyen Thi V', '1992-05-05 00:00:00', 'F', '888 Tran Hung Dao, Quan 5, TP. Ho Chi Minh', 'ntv@itd.edu.vn', '0987654321', 'ITD03');
INSERT INTO lecturer VALUES ('LT000007', 'Tran Van W', '1983-09-30 00:00:00', 'M', '777 Le Hong Phong, Quan 10, TP. Ho Chi Minh', 'tvw@itd.edu.vn', '0111222333', 'ITD03');
INSERT INTO lecturer VALUES ('LT000008', 'Pham Thi X', '1981-03-25 00:00:00', 'F', '999 Hoang Sa, Quan 3, TP. Ho Chi Minh', 'ptx@itd.edu.vn', '0333444555', 'ITD04');
INSERT INTO lecturer VALUES ('LT000009', 'Hoang Van Y', '1984-01-10 00:00:00', 'M', '123 Pham Ngu Lao, Quan 1, TP. Ho Chi Minh', 'hvy@itd.edu.vn', '0123456789', 'ITD04');
INSERT INTO lecturer VALUES ('LT000010', 'Le Thi Z', '1986-08-15 00:00:00', 'F', '456 Vo Thi Sau, Quan 3, TP. Ho Chi Minh', 'ltz@itd.edu.vn', '0987654321', 'ITD04');
INSERT INTO lecturer VALUES ('LT000011', 'Nguyen Van A', '1975-01-01 00:00:00', 'M', '123 Nguyen Van Cu, Quan 5, TP. Ho Chi Minh', 'vana@itd.edu.vn', '0111222333', 'ITD03');
INSERT INTO lecturer VALUES ('LT000012', 'Tran Thi B', '1980-05-20 00:00:00', 'F', '456 Le Van Sy, Quan 3, TP. Ho Chi Minh', 'btran@itd.edu.vn', '0333444555', 'ITD03');
INSERT INTO lecturer VALUES ('LT000013', 'John Doe', '1980-01-01 00:00:00', 'M', '123 Main St., Anytown, USA', 'johndoe@example.com', '1234567890', 'ITD01');
INSERT INTO lecturer VALUES ('LT000014', 'Jane Smith', '1985-05-15 00:00:00', 'F', '456 Elm St., Anytown, USA', 'janesmith@example.com', '2345678901', 'ITD02');
INSERT INTO lecturer VALUES ('LT000015', 'Peter Parker', '1989-07-01 00:00:00', 'M', '789 5th Ave., New York, NY', 'peterparker@example.com', '3456789012', 'ITD03');
INSERT INTO lecturer VALUES ('LT000016', 'Mary Jane Watson', '1991-09-15 00:00:00', 'F', '456 6th St., New York, NY', 'maryjanewatson@example.com', '4567890123', 'ITD04');
INSERT INTO lecturer VALUES ('LT000020', 'John Doe', '1980-01-01 00:00:00', 'M', '123 Đường Chính, Thành phố HCM', 'johndoe@example.com', '0123456789', 'ITD01');
INSERT INTO lecturer VALUES ('LT000021', 'Jane Doe', '1985-05-05 00:00:00', 'F', '456 Đường Phụ, Thành phố Hà Nội', 'janedoe@example.com', '0987654321', 'ITD01');
INSERT INTO lecturer VALUES ('LT000022', 'Nguyễn Văn A', '1975-12-31 00:00:00', 'M', '789 Đường Chính, Thành phố Đà Nẵng', 'vana@example.com', '0123456789', 'ITD01');
INSERT INTO lecturer VALUES ('LT000023', 'Trần Thị B', '1982-06-15 00:00:00', 'F', '321 Đường Phụ, Thành phố Hải Phòng', 'thib@example.com', '0987654321', 'ITD01');
INSERT INTO lecturer VALUES ('LT000024', 'Lê Văn C', '1990-03-20 00:00:00', 'M', '654 Đường Chính, Thành phố Cần Thơ', 'levanc@example.com', '0123456789', 'ITD01');
INSERT INTO lecturer VALUES ('LT000025', 'Phạm Thị D', '1988-09-10 00:00:00', 'F', '987 Đường Phụ, Thành phố Hồ Chí Minh', 'thid@example.com', '0987654321', 'ITD01');
INSERT INTO lecturer VALUES ('LT000026', 'Hoàng Văn E', '1983-11-25 00:00:00', 'M', '741 Đường Chính, Thành phố Hà Nội', 'vanhe@example.com', '0123456789', 'ITD01');
INSERT INTO lecturer VALUES ('LT000027', 'Nguyễn Thị F', '1986-07-01 00:00:00', 'F', '852 Đường Phụ, Thành phố Đà Lạt', 'thif@example.com', '0987654321', 'ITD01');
INSERT INTO lecturer VALUES ('LT000028', 'Trần Văn G', '1979-04-05 00:00:00', 'M', '963 Đường Chính, Thành phố Nha Trang', 'vang@example.com', '0123456789', 'ITD01');
INSERT INTO lecturer VALUES ('LT000029', 'Lê Thị H', '1984-08-15 00:00:00', 'F', '159 Đường Phụ, Thành phố Hải Dương', 'thih@example.com', '0987654321', 'ITD01');
CREATE TABLE `schedule` (
  `scheduleID` varchar(8) NOT NULL,
  `courseID` char(8) NOT NULL,
  `day` enum('mon','tue','wed','thu','fri') NOT NULL,
  `time` time NOT NULL,
  `classroomID` char(8) NOT NULL,
  `lecturerID` char(8) DEFAULT NULL,
  `semester` char(15) DEFAULT NULL,
  PRIMARY KEY (`scheduleID`),
  KEY `lecturerID` (`lecturerID`),
  KEY `courseID` (`courseID`),
  KEY `classroomID` (`classroomID`),
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`lecturerID`) REFERENCES `lecturer` (`lecturerID`),
  CONSTRAINT `schedule_ibfk_2` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`),
  CONSTRAINT `schedule_ibfk_3` FOREIGN KEY (`classroomID`) REFERENCES `classroom` (`classroomID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO schedule VALUES ('SC10', 'DC114', 'tue', '10:00:00', 'C007', 'LT000002', '2023.2');
INSERT INTO schedule VALUES ('SC6', 'CS115', 'thu', '9:00:00', 'C002', 'LT000001', '2023.2');
INSERT INTO schedule VALUES ('SC7', 'CN101', 'wed', '14:00:00', 'C003', 'LT000001', '2023.2');
INSERT INTO schedule VALUES ('SC8', 'CN112', 'fri', '11:00:00', 'C004', 'LT000001', '2023.2');
INSERT INTO schedule VALUES ('SC9', 'DC113', 'mon', '7:00:00', 'C013', 'LT000002', '2023.2');
CREATE TABLE `student` (
  `studentID` char(8) NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `dateOfBirth` datetime NOT NULL,
  `gender` char(1) NOT NULL,
  `address` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `phoneNumber` char(10) NOT NULL,
  `classID` char(8) DEFAULT NULL,
  PRIMARY KEY (`studentID`),
  KEY `FK1` (`classID`),
  CONSTRAINT `FK1` FOREIGN KEY (`classID`) REFERENCES `studentclass` (`classID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO student VALUES ('ST000001', 'Nguyễn Văn A', '2000-01-01 00:00:00', 'M', 'Hà Nội', 'nguyenvana@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000002', 'Trần Thị B', '2000-02-02 00:00:00', 'F', 'Hải Phòng', 'tranthib@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000003', 'Lê Văn C', '2000-03-03 00:00:00', 'M', 'Hồ Chí Minh', 'levanc@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000004', 'Phạm Thị D', '2000-04-04 00:00:00', 'F', 'Đà Nẵng', 'phamthid@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000005', 'Hoàng Văn E', '2000-05-05 00:00:00', 'M', 'Hà Tĩnh', 'hoangvane@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000006', 'Nguyễn Thị F', '2000-06-06 00:00:00', 'F', 'Hà Nội', 'nguyenthif@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000007', 'Trần Văn G', '2000-07-07 00:00:00', 'M', 'Hải Phòng', 'tranvang@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000008', 'Lê Thị H', '2000-08-08 00:00:00', 'F', 'Hồ Chí Minh', 'lethih@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000009', 'Phạm Văn I', '2000-09-09 00:00:00', 'M', 'Đà Nẵng', 'phamvani@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000010', 'Hoàng Thị K', '2000-10-10 00:00:00', 'F', 'Hà Tĩnh', 'hoangthik@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000011', 'Nguyễn Văn L', '2000-11-11 00:00:00', 'M', 'Hà Nội', 'nguyenvanl@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000012', 'Trần Thị M', '2000-12-12 00:00:00', 'F', 'Hải Phòng', 'tranthim@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000013', 'Lê Văn N', '2001-01-01 00:00:00', 'M', 'Hồ Chí Minh', 'levann@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000014', 'Phạm Thị O', '2001-02-02 00:00:00', 'F', 'Đà Nẵng', 'phamthio@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000015', 'Hoàng Văn P', '2001-03-03 00:00:00', 'M', 'Hà Tĩnh', 'hoangvanp@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000016', 'Nguyễn Thị Q', '2001-04-04 00:00:00', 'F', 'Hà Nội', 'nguyenthiq@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000017', 'Trần Văn R', '2001-05-05 00:00:00', 'M', 'Hải Phòng', 'tranvanr@gmail.com', '0123456789', 'CNTT2021');
INSERT INTO student VALUES ('ST000018', 'Nguyễn Văn An', '2003-01-01 00:00:00', 'M', 'Số 1, Đường A, Quận B, Hà Nội', 'hs1@example.com', '123456789', 'CNTT2020');
INSERT INTO student VALUES ('ST000019', 'Trần Thị Bình', '2003-01-02 00:00:00', 'F', 'Số 2, Đường X, Quận Y, Hồ Chí Minh', 'hs2@example.com', '234567890', 'CNTT2020');
INSERT INTO student VALUES ('ST000020', 'Lê Văn Cường', '2003-01-03 00:00:00', 'M', 'Số 3, Đường Z, Quận T, Đà Nẵng', 'hs3@example.com', '345678901', 'CNTT2020');
INSERT INTO student VALUES ('ST000021', 'Phạm Thị Đào', '2003-01-04 00:00:00', 'F', 'Số 4, Đường M, Quận N, Hải Phòng', 'hs4@example.com', '456789012', 'CNTT2020');
INSERT INTO student VALUES ('ST000022', 'Hoàng Văn Em', '2003-01-05 00:00:00', 'M', 'Số 5, Đường E, Quận F, Cần Thơ', 'hs5@example.com', '567890123', 'CNTT2020');
INSERT INTO student VALUES ('ST000023', 'Vũ Thị F', '2003-01-06 00:00:00', 'F', 'Số 6, Đường G, Quận H, Đồng Nai', 'hs6@example.com', '678901234', 'CNTT2020');
INSERT INTO student VALUES ('ST000024', 'Nguyễn Văn G', '2003-01-07 00:00:00', 'M', 'Số 7, Đường I, Quận J, Thanh Hóa', 'hs7@example.com', '789012345', 'CNTT2020');
INSERT INTO student VALUES ('ST000025', 'Trần Thị H', '2003-01-08 00:00:00', 'F', 'Số 8, Đường K, Quận L, Nghệ An', 'hs8@example.com', '890123456', 'CNTT2020');
INSERT INTO student VALUES ('ST000026', 'Lê Văn I', '2003-01-09 00:00:00', 'M', 'Số 9, Đường O, Quận P, Hà Tĩnh', 'hs9@example.com', '901234567', 'CNTT2020');
INSERT INTO student VALUES ('ST000027', 'Phạm Thị J', '2003-01-10 00:00:00', 'F', 'Số 10, Đường Q, Quận R, Bình Định', 'hs10@example.com', '012345678', 'CNTT2020');
INSERT INTO student VALUES ('ST000028', 'Hoàng Văn K', '2003-01-11 00:00:00', 'M', 'Số 11, Đường S, Quận T, Đồng Tháp', 'hs11@example.com', '123456789', 'CNTT2020');
INSERT INTO student VALUES ('ST000029', 'Vũ Thị L', '2003-01-12 00:00:00', 'F', 'Số 12, Đường U, Quận V, Long An', 'hs12@example.com', '234567890', 'CNTT2020');
INSERT INTO student VALUES ('ST000030', 'Nguyễn Văn M', '2003-01-13 00:00:00', 'M', 'Số 13, Đường W, Quận X, An Giang', 'hs13@example.com', '345678901', 'CNTT2020');
INSERT INTO student VALUES ('ST000031', 'Trần Thị N', '2003-01-14 00:00:00', 'F', 'Số 14, Đường Y, Quận Z, Bà Rịa - Vũng Tàu', 'hs14@example.com', '456789012', 'CNTT2020');
INSERT INTO student VALUES ('ST000032', 'Lê Văn O', '2003-01-15 00:00:00', 'M', 'Số 15, Đường A1, Quận B1, Bắc Giang', 'hs15@example.com', '567890123', 'CNTT2020');
INSERT INTO student VALUES ('ST000033', 'Phạm Thị P', '2003-01-16 00:00:00', 'F', 'Số 16, Đường C1, Quận D1, Bắc Kạn', 'hs16@example.com', '678901234', 'CNTT2020');
INSERT INTO student VALUES ('ST000034', 'Hoàng Văn Q', '2003-01-17 00:00:00', 'M', 'Số 17, Đường E1, Quận F1, Bạc Liêu', 'hs17@example.com', '789012345', 'CNTT2020');
INSERT INTO student VALUES ('ST000035', 'Vũ Thị R', '2003-01-18 00:00:00', 'F', 'Số 18, Đường G1, Quận H1, Bắc Ninh', 'hs18@example.com', '890123456', 'CNTT2020');
INSERT INTO student VALUES ('ST000036', 'Nguyễn Văn S', '2003-01-19 00:00:00', 'M', 'Số 19, Đường I1, Quận J1, Bến Tre', 'hs19@example.com', '901234567', 'CNTT2020');
INSERT INTO student VALUES ('ST000037', 'Trần Thị T', '2003-01-20 00:00:00', 'F', 'Số 20, Đường K1, Quận L1, Bình Dương', 'hs20@example.com', '012345678', 'CNTT2020');
INSERT INTO student VALUES ('ST000038', 'Lê Văn U', '2003-01-21 00:00:00', 'M', 'Số 21, Đường M1, Quận N1, Bình Phước', 'hs21@example.com', '123456789', 'CNTT2020');
INSERT INTO student VALUES ('ST000039', 'Phạm Thị V', '2003-01-22 00:00:00', 'F', 'Số 22, Đường O1, Quận P1, Cà Mau', 'hs22@example.com', '234567890', 'CNTT2020');
INSERT INTO student VALUES ('ST000040', 'Hoàng Văn W', '2003-01-23 00:00:00', 'M', 'Số 23, Đường Q1, Quận R1, Cao Bằng', 'hs23@example.com', '345678901', 'CNTT2020');
INSERT INTO student VALUES ('ST000041', 'Vũ Thị X', '2003-01-24 00:00:00', 'F', 'Số 24, Đường S1, Quận T1, Đắk Lắk', 'hs24@example.com', '456789012', 'CNTT2020');
INSERT INTO student VALUES ('ST000042', 'Nguyễn Văn Y', '2003-01-25 00:00:00', 'M', 'Số 25, Đường U1, Quận V1, Đắk Nông', 'hs25@example.com', '567890123', 'CNTT2020');
INSERT INTO student VALUES ('ST000043', 'Trần Thị Z', '2003-01-26 00:00:00', 'F', 'Số 26, Đường W1, Quận X1, Điện Biên', 'hs26@example.com', '678901234', 'CNTT2020');
INSERT INTO student VALUES ('ST000044', 'Lê Văn AA', '2003-01-27 00:00:00', 'M', 'Số 27, Đường Y1, Quận Z1, Đồng Tháp', 'hs27@example.com', '789012345', 'CNTT2020');
INSERT INTO student VALUES ('ST000045', 'Phạm Thị BB', '2003-01-28 00:00:00', 'F', 'Số 28, Đường A2, Quận B2, Gia Lai', 'hs28@example.com', '890123456', 'CNTT2020');
INSERT INTO student VALUES ('ST000046', 'Hoàng Văn CC', '2003-01-29 00:00:00', 'M', 'Số 29, Đường C2, Quận D2, Hà Giang', 'hs29@example.com', '901234567', 'CNTT2020');
INSERT INTO student VALUES ('ST000047', 'Vũ Thị DD', '2003-01-30 00:00:00', 'F', 'Số 30, Đường E2, Quận F2, Hà Nam', 'hs30@example.com', '012345678', 'CNTT2020');
CREATE TABLE `student_schedule` (
  `studentID` varchar(8) NOT NULL,
  `scheduleid` varchar(8) NOT NULL,
  PRIMARY KEY (`studentID`,`scheduleid`),
  KEY `scheduleid` (`scheduleid`),
  CONSTRAINT `student_schedule_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `student` (`studentID`),
  CONSTRAINT `student_schedule_ibfk_2` FOREIGN KEY (`scheduleid`) REFERENCES `schedule` (`scheduleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO student_schedule VALUES ('ST000001', 'SC10');
INSERT INTO student_schedule VALUES ('ST000001', 'SC6');
INSERT INTO student_schedule VALUES ('ST000001', 'SC7');
INSERT INTO student_schedule VALUES ('ST000001', 'SC8');
INSERT INTO student_schedule VALUES ('ST000001', 'SC9');
CREATE TABLE `studentclass` (
  `classID` char(8) NOT NULL,
  `academicYear` year NOT NULL,
  `numberOfStudent` int DEFAULT NULL,
  `lecturerID` char(8) NOT NULL,
  PRIMARY KEY (`classID`),
  KEY `lecturerID` (`lecturerID`),
  CONSTRAINT `studentclass_ibfk_1` FOREIGN KEY (`lecturerID`) REFERENCES `lecturer` (`lecturerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO studentclass VALUES ('CNTT2020', '2020', '30', 'LT000005');
INSERT INTO studentclass VALUES ('CNTT2021', '2021', '17', 'LT000001');
INSERT INTO studentclass VALUES ('KHMT2020', '2020', 'None', 'LT000009');
INSERT INTO studentclass VALUES ('KHMT2021', '2021', 'None', 'LT000013');
INSERT INTO studentclass VALUES ('MMT2021', '2022', 'None', 'LT000016');
CREATE TABLE `testschedule` (
  `scheduleID` varchar(8) NOT NULL,
  `classroomID` char(8) NOT NULL,
  `Time` datetime NOT NULL,
  `CourseID` char(8) DEFAULT NULL,
  `LecturerID` char(8) DEFAULT NULL,
  PRIMARY KEY (`classroomID`,`Time`,`scheduleID`),
  KEY `CourseID` (`CourseID`),
  KEY `scheduleID` (`scheduleID`),
  KEY `LecturerID` (`LecturerID`),
  CONSTRAINT `testschedule_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `course` (`courseID`),
  CONSTRAINT `testschedule_ibfk_2` FOREIGN KEY (`classroomID`) REFERENCES `classroom` (`classroomID`),
  CONSTRAINT `testschedule_ibfk_3` FOREIGN KEY (`scheduleID`) REFERENCES `schedule` (`scheduleID`),
  CONSTRAINT `testschedule_ibfk_4` FOREIGN KEY (`LecturerID`) REFERENCES `lecturer` (`lecturerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO testschedule VALUES ('SC10', 'C001', '2023-06-06 09:00:00', 'DC114', 'LT000001');
INSERT INTO testschedule VALUES ('SC7', 'C001', '2023-08-06 08:00:00', 'CN101', 'LT000004');
INSERT INTO testschedule VALUES ('SC6', 'C001', '2023-08-07 09:00:00', 'CS115', 'LT000001');
CREATE TABLE `tuitionfee` (
  `TuitionFee` decimal(10,0) NOT NULL,
  `Status` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `StudentID` char(8) NOT NULL,
  `sumcredit` int DEFAULT NULL,
  PRIMARY KEY (`StudentID`,`TuitionFee`),
  CONSTRAINT `tuitionfee_ibfk_1` FOREIGN KEY (`StudentID`) REFERENCES `student` (`studentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO tuitionfee VALUES ('4000000', 'unpaid', 'st000001', '10');
