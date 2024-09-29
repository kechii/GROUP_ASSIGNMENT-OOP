import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
import re

class SchoolManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("School Management System")
        self.master.geometry("1000x700")
        
        self.db = Database('school.db')
        
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.students_tab = ttk.Frame(self.notebook)
        self.courses_tab = ttk.Frame(self.notebook)
        self.instructors_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.students_tab, text="Students")
        self.notebook.add(self.courses_tab, text="Courses")
        self.notebook.add(self.instructors_tab, text="Instructors")

        self.create_students_widgets()
        self.create_courses_widgets()
        self.create_instructors_widgets()

    def create_students_widgets(self):
        # Student Information
        ttk.Label(self.students_tab, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.student_id = ttk.Entry(self.students_tab)
        self.student_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.students_tab, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.student_name = ttk.Entry(self.students_tab)
        self.student_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.students_tab, text="Age:").grid(row=2, column=0, padx=5, pady=5)
        self.student_age = ttk.Entry(self.students_tab)
        self.student_age.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.students_tab, text="Grade:").grid(row=3, column=0, padx=5, pady=5)
        self.student_grade = ttk.Entry(self.students_tab)
        self.student_grade.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.students_tab, text="Privacy Consent:").grid(row=4, column=0, padx=5, pady=5)
        self.student_privacy = tk.BooleanVar()
        ttk.Checkbutton(self.students_tab, variable=self.student_privacy).grid(row=4, column=1, padx=5, pady=5)

        # Privacy Policy
        ttk.Label(self.students_tab, text="Privacy Policy:").grid(row=5, column=0, padx=5, pady=5)
        self.privacy_policy = tk.Text(self.students_tab, height=3, width=50)
        self.privacy_policy.insert(tk.END, "By providing consent, you agree to the collection and processing of your personal data in accordance with our privacy policy.")
        self.privacy_policy.config(state=tk.DISABLED)
        self.privacy_policy.grid(row=5, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(self.students_tab, text="Add", command=self.add_student).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(self.students_tab, text="Update", command=self.update_student).grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(self.students_tab, text="Delete", command=self.delete_student).grid(row=7, column=0, padx=5, pady=5)
        ttk.Button(self.students_tab, text="View All", command=self.view_students).grid(row=7, column=1, padx=5, pady=5)

        # Treeview
        self.students_tree = ttk.Treeview(self.students_tab, columns=("ID", "Name", "Age", "Grade", "Privacy"), show="headings")
        self.students_tree.heading("ID", text="ID")
        self.students_tree.heading("Name", text="Name")
        self.students_tree.heading("Age", text="Age")
        self.students_tree.heading("Grade", text="Grade")
        self.students_tree.heading("Privacy", text="Privacy")
        self.students_tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        self.students_tree.bind("<<TreeviewSelect>>", self.on_student_select)

    def create_courses_widgets(self):
        # Course Information
        ttk.Label(self.courses_tab, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.course_id = ttk.Entry(self.courses_tab)
        self.course_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.courses_tab, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.course_name = ttk.Entry(self.courses_tab)
        self.course_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.courses_tab, text="Code:").grid(row=2, column=0, padx=5, pady=5)
        self.course_code = ttk.Entry(self.courses_tab)
        self.course_code.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.courses_tab, text="Instructor ID:").grid(row=3, column=0, padx=5, pady=5)
        self.course_instructor = ttk.Entry(self.courses_tab)
        self.course_instructor.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(self.courses_tab, text="Add", command=self.add_course).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.courses_tab, text="Update", command=self.update_course).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(self.courses_tab, text="Delete", command=self.delete_course).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self.courses_tab, text="View All", command=self.view_courses).grid(row=5, column=1, padx=5, pady=5)

        # Treeview
        self.courses_tree = ttk.Treeview(self.courses_tab, columns=("ID", "Name", "Code", "Instructor"), show="headings")
        self.courses_tree.heading("ID", text="ID")
        self.courses_tree.heading("Name", text="Name")
        self.courses_tree.heading("Code", text="Code")
        self.courses_tree.heading("Instructor", text="Instructor ID")
        self.courses_tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.courses_tree.bind("<<TreeviewSelect>>", self.on_course_select)

    def create_instructors_widgets(self):
        # Instructor Information
        ttk.Label(self.instructors_tab, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.instructor_id = ttk.Entry(self.instructors_tab)
        self.instructor_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.instructors_tab, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.instructor_name = ttk.Entry(self.instructors_tab)
        self.instructor_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.instructors_tab, text="Department:").grid(row=2, column=0, padx=5, pady=5)
        self.instructor_department = ttk.Entry(self.instructors_tab)
        self.instructor_department.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.instructors_tab, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.instructor_email = ttk.Entry(self.instructors_tab)
        self.instructor_email.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(self.instructors_tab, text="Add", command=self.add_instructor).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.instructors_tab, text="Update", command=self.update_instructor).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(self.instructors_tab, text="Delete", command=self.delete_instructor).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self.instructors_tab, text="View All", command=self.view_instructors).grid(row=5, column=1, padx=5, pady=5)

        # Treeview
        self.instructors_tree = ttk.Treeview(self.instructors_tab, columns=("ID", "Name", "Department", "Email"), show="headings")
        self.instructors_tree.heading("ID", text="ID")
        self.instructors_tree.heading("Name", text="Name")
        self.instructors_tree.heading("Department", text="Department")
        self.instructors_tree.heading("Email", text="Email")
        self.instructors_tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.instructors_tree.bind("<<TreeviewSelect>>", self.on_instructor_select)

    # Student CRUD operations
    def add_student(self):
        name = self.student_name.get()
        age = self.student_age.get()
        grade = self.student_grade.get()
        privacy = self.student_privacy.get()

        try:
            self.validate_student_input(name, age, grade)
            
            if not privacy:
                raise ValueError("Privacy consent must be given to proceed")

            self.db.add_student(name, int(age), grade, privacy)
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_student_fields()
            self.view_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student(self):
        student_id = self.student_id.get()
        name = self.student_name.get()
        age = self.student_age.get()
        grade = self.student_grade.get()
        privacy = self.student_privacy.get()

        try:
            self.validate_student_input(name, age, grade)
            
            if not privacy:
                raise ValueError("Privacy consent must be given to proceed")

            if not student_id:
                raise ValueError("Please select a student to update")

            self.db.update_student(int(student_id), name, int(age), grade, privacy)
            messagebox.showinfo("Success", "Student updated successfully!")
            self.clear_student_fields()
            self.view_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        student_id = self.student_id.get()
        if student_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this student? This action cannot be undone."):
                try:
                    self.db.delete_student(int(student_id))
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    self.clear_student_fields()
                    self.view_students()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please select a student to delete")

    def view_students(self):
        for i in self.students_tree.get_children():
            self.students_tree.delete(i)
        
        students = self.db.get_all_students()
        for student in students:
            display_info = (student[0], student[1], student[2], student[3], "Yes" if student[4] else "No")
            self.students_tree.insert("", "end", values=display_info)

    def validate_student_input(self, name, age, grade):
        if not name or not age or not grade:
            raise ValueError("All fields must be filled")
        
        if not name.replace(" ", "").isalpha():
            raise ValueError("Name should only contain alphabets and spaces")
        
        if not age.isdigit() or int(age) < 0 or int(age) > 120:
            raise ValueError("Age should be a positive number between 0 and 120")
        
        if not grade.isalnum():
            raise ValueError("Grade should be alphanumeric")

    def on_student_select(self, event):
        selected_item = self.students_tree.selection()[0]
        student = self.students_tree.item(selected_item)['values']
        self.student_id.delete(0, tk.END)
        self.student_id.insert(0, student[0])
        self.student_name.delete(0, tk.END)
        self.student_name.insert(0, student[1])
        self.student_age.delete(0, tk.END)
        self.student_age.insert(0, student[2])
        self.student_grade.delete(0, tk.END)
        self.student_grade.insert(0, student[3])
        self.student_privacy.set(student[4] == "Yes")

    def clear_student_fields(self):
        self.student_id.delete(0, tk.END)
        self.student_name.delete(0, tk.END)
        self.student_age.delete(0, tk.END)
        self.student_grade.delete(0, tk.END)
        self.student_privacy.set(False)

    # Course CRUD operations
    def add_course(self):
        name = self.course_name.get()
        code = self.course_code.get()
        instructor_id = self.course_instructor.get()

        try:
            self.validate_course_input(name, code, instructor_id)

            self.db.add_course(name, code, int(instructor_id))
            messagebox.showinfo("Success", "Course added successfully!")
            self.clear_course_fields()
            self.view_courses()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_course(self):
        course_id = self.course_id.get()
        name = self.course_name.get()
        code = self.course_code.get()
        instructor_id = self.course_instructor.get()

        try:
            self.validate_course_input(name, code, instructor_id)

            if not course_id:
                raise ValueError("Please select a course to update")

            self.db.update_course(int(course_id), name, code, int(instructor_id))
            messagebox.showinfo("Success", "Course updated successfully!")
            self.clear_course_fields()
            self.view_courses()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_course(self):
        course_id = self.course_id.get()
        if course_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this course? This action cannot be undone."):
                try:
                    self.db.delete_course(int(course_id))
                    messagebox.showinfo("Success", "Course deleted successfully!")
                    self.clear_course_fields()
                    self.view_courses()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please select a course to delete")

    def view_courses(self):
        for i in self.courses_tree.get_children():
            self.courses_tree.delete(i)
        
        courses = self.db.get_all_courses()
        for course in courses:
            self.courses_tree.insert("", "end", values=course)

    def validate_course_input(self, name, code, instructor_id):
        if not name or not code or not instructor_id:
            raise ValueError("All fields must be filled")
        
        if not name.replace(" ", "").isalnum():
            raise ValueError("Course name should only contain alphanumeric characters and spaces")
        
        # Updated course code validation
        if not re.match(r'^[A-Za-z]{2,4}\d{3,4}$', code):
            raise ValueError("Course code should be 2-4 letters followed by 3-4 numbers (e.g., CS101 or MATH2023)")
        
        if not instructor_id.isdigit():
            raise ValueError("Instructor ID should be a positive integer")

    def on_course_select(self, event):
        selected_item = self.courses_tree.selection()[0]
        course = self.courses_tree.item(selected_item)['values']
        self.course_id.delete(0, tk.END)
        self.course_id.insert(0, course[0])
        self.course_name.delete(0, tk.END)
        self.course_name.insert(0, course[1])
        self.course_code.delete(0, tk.END)
        self.course_code.insert(0, course[2])
        self.course_instructor.delete(0, tk.END)
        self.course_instructor.insert(0, course[3])

    def clear_course_fields(self):
        self.course_id.delete(0, tk.END)
        self.course_name.delete(0, tk.END)
        self.course_code.delete(0, tk.END)
        self.course_instructor.delete(0, tk.END)

    # Instructor CRUD operations
    def add_instructor(self):
        name = self.instructor_name.get()
        department = self.instructor_department.get()
        email = self.instructor_email.get()

        try:
            self.validate_instructor_input(name, department, email)

            self.db.add_instructor(name, department, email)
            messagebox.showinfo("Success", "Instructor added successfully!")
            self.clear_instructor_fields()
            self.view_instructors()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_instructor(self):
        instructor_id = self.instructor_id.get()
        name = self.instructor_name.get()
        department = self.instructor_department.get()
        email = self.instructor_email.get()

        try:
            self.validate_instructor_input(name, department, email)

            if not instructor_id:
                raise ValueError("Please select an instructor to update")

            self.db.update_instructor(int(instructor_id), name, department, email)
            messagebox.showinfo("Success", "Instructor updated successfully!")
            self.clear_instructor_fields()
            self.view_instructors()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_instructor(self):
        instructor_id = self.instructor_id.get()
        if instructor_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this instructor? This action cannot be undone."):
                try:
                    self.db.delete_instructor(int(instructor_id))
                    messagebox.showinfo("Success", "Instructor deleted successfully!")
                    self.clear_instructor_fields()
                    self.view_instructors()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please select an instructor to delete")

    def view_instructors(self):
        for i in self.instructors_tree.get_children():
            self.instructors_tree.delete(i)
        
        instructors = self.db.get_all_instructors()
        for instructor in instructors:
            self.instructors_tree.insert("", "end", values=instructor)

    def validate_instructor_input(self, name, department, email):
        if not name or not department or not email:
            raise ValueError("All fields must be filled")
        
        if not name.replace(" ", "").isalpha():
            raise ValueError("Instructor name should only contain alphabets and spaces")
        
        if not department.replace(" ", "").isalpha():
            raise ValueError("Department should only contain alphabets and spaces")
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

    def on_instructor_select(self, event):
        selected_item = self.instructors_tree.selection()[0]
        instructor = self.instructors_tree.item(selected_item)['values']
        self.instructor_id.delete(0, tk.END)
        self.instructor_id.insert(0, instructor[0])
        self.instructor_name.delete(0, tk.END)
        self.instructor_name.insert(0, instructor[1])
        self.instructor_department.delete(0, tk.END)
        self.instructor_department.insert(0, instructor[2])
        self.instructor_email.delete(0, tk.END)
        self.instructor_email.insert(0, instructor[3])

    def clear_instructor_fields(self):
        self.instructor_id.delete(0, tk.END)
        self.instructor_name.delete(0, tk.END)
        self.instructor_department.delete(0, tk.END)
        self.instructor_email.delete(0, tk.END)

    # Additional utility methods
    def get_courses_by_instructor(self):
        instructor_id = self.instructor_id.get()
        if instructor_id:
            courses = self.db.get_courses_by_instructor(int(instructor_id))
            if courses:
                course_list = "\n".join([f"{c[1]} ({c[2]})" for c in courses])
                messagebox.showinfo("Courses", f"Courses taught by this instructor:\n\n{course_list}")
            else:
                messagebox.showinfo("Courses", "This instructor is not teaching any courses.")
        else:
            messagebox.showerror("Error", "Please select an instructor first")

    def get_students_by_course(self):
        course_id = self.course_id.get()
        if course_id:
            students = self.db.get_students_by_course(int(course_id))
            if students:
                student_list = "\n".join([f"{s[1]} (Age: {s[2]}, Grade: {s[3]})" for s in students])
                messagebox.showinfo("Students", f"Students enrolled in this course:\n\n{student_list}")
            else:
                messagebox.showinfo("Students", "No students are enrolled in this course.")
        else:
            messagebox.showerror("Error", "Please select a course first")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementSystem(root)
    root.mainloop()