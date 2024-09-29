import sqlite3
import os
from cryptography.fernet import Fernet, InvalidToken

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        # Use a persistent key
        key_file = 'encryption_key.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.key)
        
        self.cipher_suite = Fernet(self.key)
        
        self.create_students_table()
        self.create_courses_table()
        self.create_instructors_table()

    def create_students_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Students_1731
                            (id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            age INTEGER,
                            grade TEXT,
                            privacy_consent BOOLEAN)''')
        self.conn.commit()

    def create_courses_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Courses_1731
                            (id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            code TEXT NOT NULL,
                            instructor_id INTEGER,
                            FOREIGN KEY (instructor_id) REFERENCES Instructors_1731(id))''')
        self.conn.commit()

    def create_instructors_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Instructors_1731
                            (id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            department TEXT,
                            email TEXT)''')
        self.conn.commit()

    def encrypt_data(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt_data(self, data):
        try:
            return self.cipher_suite.decrypt(data).decode()
        except InvalidToken:
            print(f"Failed to decrypt data: {data}")
            raise

    def add_student(self, name, age, grade, privacy_consent):
        encrypted_name = self.encrypt_data(name)
        self.cursor.execute('''INSERT INTO Students_1731 (name, age, grade, privacy_consent)
                            VALUES (?, ?, ?, ?)''', (encrypted_name, age, grade, privacy_consent))
        self.conn.commit()

    def get_student(self, student_id):
        self.cursor.execute("SELECT * FROM Students_1731 WHERE id=?", (student_id,))
        student = self.cursor.fetchone()
        if student:
            return (student[0], self.decrypt_data(student[1]), student[2], student[3], student[4])
        return None

    def update_student(self, student_id, name, age, grade, privacy_consent):
        encrypted_name = self.encrypt_data(name)
        self.cursor.execute('''UPDATE Students_1731 SET name=?, age=?, grade=?, privacy_consent=?
                            WHERE id=?''', (encrypted_name, age, grade, privacy_consent, student_id))
        self.conn.commit()

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM Students_1731 WHERE id=?", (student_id,))
        self.conn.commit()

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM Students_1731")
        students = self.cursor.fetchall()
        return [(s[0], self.decrypt_data(s[1]), s[2], s[3], s[4]) for s in students]

    def add_course(self, name, code, instructor_id):
        self.cursor.execute('''INSERT INTO Courses_1731 (name, code, instructor_id)
                            VALUES (?, ?, ?)''', (name, code, instructor_id))
        self.conn.commit()

    def get_course(self, course_id):
        self.cursor.execute("SELECT * FROM Courses_1731 WHERE id=?", (course_id,))
        return self.cursor.fetchone()

    def update_course(self, course_id, name, code, instructor_id):
        self.cursor.execute('''UPDATE Courses_1731 SET name=?, code=?, instructor_id=?
                            WHERE id=?''', (name, code, instructor_id, course_id))
        self.conn.commit()

    def delete_course(self, course_id):
        self.cursor.execute("DELETE FROM Courses_1731 WHERE id=?", (course_id,))
        self.conn.commit()

    def get_all_courses(self):
        self.cursor.execute("SELECT * FROM Courses_1731")
        return self.cursor.fetchall()

    def add_instructor(self, name, department, email):
        self.cursor.execute('''INSERT INTO Instructors_1731 (name, department, email)
                            VALUES (?, ?, ?)''', (name, department, email))
        self.conn.commit()

    def get_instructor(self, instructor_id):
        self.cursor.execute("SELECT * FROM Instructors_1731 WHERE id=?", (instructor_id,))
        return self.cursor.fetchone()

    def update_instructor(self, instructor_id, name, department, email):
        self.cursor.execute('''UPDATE Instructors_1731 SET name=?, department=?, email=?
                            WHERE id=?''', (name, department, email, instructor_id))
        self.conn.commit()

    def delete_instructor(self, instructor_id):
        self.cursor.execute("DELETE FROM Instructors_1731 WHERE id=?", (instructor_id,))
        self.conn.commit()

    def get_all_instructors(self):
        self.cursor.execute("SELECT * FROM Instructors_1731")
        return self.cursor.fetchall()

    def get_courses_by_instructor(self, instructor_id):
        self.cursor.execute("SELECT * FROM Courses_1731 WHERE instructor_id=?", (instructor_id,))
        return self.cursor.fetchall()

    def get_students_by_course(self, course_id):
        self.cursor.execute('''SELECT s.* FROM Students_1731 s
                            JOIN StudentCourses_1731 sc ON s.id = sc.student_id
                            WHERE sc.course_id = ?''', (course_id,))
        students = self.cursor.fetchall()
        return [(s[0], self.decrypt_data(s[1]), s[2], s[3], s[4]) for s in students]

    def close(self):
        self.conn.close()