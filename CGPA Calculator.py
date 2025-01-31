import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
import ttkthemes
from PIL import Image, ImageTk

class Student:
    def __init__(self, name: str, father_name: str, enrollment: str, roll_no: int, degree: str):
        self.name = name
        self.father_name = father_name
        self.enrollment = enrollment
        self.roll_no = roll_no
        self.degree = degree

class Course:
    def __init__(self, name: str, marks: float, credit_hours: int):
        self.name = name
        self.marks = marks
        self.credit_hours = credit_hours
        self.grade = self._calculate_grade()
        self.grade_points = self._get_grade_points()
    
    def _calculate_grade(self) -> str:
        if self.marks >= 88: return "A"
        elif self.marks >= 81: return "B+"
        elif self.marks >= 74: return "B"
        elif self.marks >= 67: return "C+"
        elif self.marks >= 60: return "C"
        else: return "F"
    
    def _get_grade_points(self) -> float:
        grade_points = {
            "A": 4.0, "B+": 3.5, "B": 3.0,
            "C+": 2.5, "C": 2.0, "F": 0.0
        }
        return grade_points[self.grade]

class GPACalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Apply the modern theme
        self.style = ttkthemes.ThemedStyle(self)
        self.style.set_theme("arc")  # Modern looking theme
        
        self.title("Iqra University GPA Calculator")
        self.geometry("1200x800")
        self.configure(bg='#f0f0f0')
        
        self.student = None
        self.courses: Dict[int, Course] = {}
        self.course_rows = []  # To keep track of dynamic course rows
        
        # Create main container with padding
        self.main_container = ttk.Frame(self, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self._create_header()
        self._create_student_frame()
        self._create_courses_frame()
        self._create_buttons_frame()
        
    def _create_header(self):
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Load and display the logo image - specify full path
        logo_path = "C:/Users/Lenovo/Desktop/iqra_logo.jpg"  # Replace with your actual path
        # OR use relative path from your script location
        # logo_path = "../images/iqra_logo.jpg"
        
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((600, 150), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        
        logo_label = ttk.Label(header_frame, image=self.logo_photo)
        logo_label.pack(pady=10)
    def _create_student_frame(self):
        student_frame = ttk.LabelFrame(
            self.main_container, 
            text="Student Information", 
            padding=20
        )
        student_frame.pack(fill='x', pady=(0, 20))
        
        # Create two columns for better layout
        left_frame = ttk.Frame(student_frame)
        right_frame = ttk.Frame(student_frame)
        left_frame.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 10))
        right_frame.pack(side=tk.LEFT, expand=True, fill='x', padx=(10, 0))
        
        # Student information fields
        self.student_entries = {}
        
        # Left column fields
        self._create_entry_field(left_frame, "Name:", "name", 0)
        self._create_entry_field(left_frame, "Father's Name:", "father_name", 1)
        self._create_entry_field(left_frame, "Enrollment No:", "enrollment", 2)
        
        # Right column fields
        self._create_entry_field(right_frame, "Roll No:", "roll_no", 0)
        self._create_degree_field(right_frame, 1)

    def _create_entry_field(self, parent, label_text, key, row):
        ttk.Label(
            parent, 
            text=label_text,
            font=('Helvetica', 10)
        ).grid(row=row, column=0, padx=5, pady=5, sticky='e')
        
        self.student_entries[key] = ttk.Entry(parent, width=30)
        self.student_entries[key].grid(row=row, column=1, padx=5, pady=5, sticky='w')

    def _create_degree_field(self, parent, row):
        ttk.Label(
            parent, 
            text="Degree:",
            font=('Helvetica', 10)
        ).grid(row=row, column=0, padx=5, pady=5, sticky='e')
        
        self.student_entries["degree"] = ttk.Combobox(
            parent,
            values=["BBA", "BS(CS)", "BS(SE)", "BS(EE)"],
            state="readonly",
            width=27
        )
        self.student_entries["degree"].grid(row=row, column=1, padx=5, pady=5, sticky='w')

    def _create_courses_frame(self):
        self.courses_frame = ttk.LabelFrame(
            self.main_container, 
            text="Course Information", 
            padding=20
        )
        self.courses_frame.pack(fill='x', pady=(0, 20))
        
        # Headers with better styling
        headers = ["Course Name", "Marks", "Credit Hours", ""]
        for i, header in enumerate(headers):
            ttk.Label(
                self.courses_frame, 
                text=header,
                font=('Helvetica', 10, 'bold')
            ).grid(row=0, column=i, padx=5, pady=(0, 10))
        
        # Initial course row
        self._add_course_row()

    def _add_course_row(self):
        row = len(self.course_rows) + 1
        course_frame = ttk.Frame(self.courses_frame)
        course_frame.grid(row=row, column=0, columnspan=4, pady=5, sticky='ew')
        
        # Course name entry
        name_entry = ttk.Entry(course_frame, width=30)
        name_entry.pack(side=tk.LEFT, padx=5)
        
        # Marks entry
        marks_entry = ttk.Entry(course_frame, width=10)
        marks_entry.pack(side=tk.LEFT, padx=5)
        
        # Credit hours combobox
        credits_combo = ttk.Combobox(
            course_frame,
            values=["1", "2", "3", "4"],
            state="readonly",
            width=5
        )
        credits_combo.pack(side=tk.LEFT, padx=5)
        
        # Remove button
        remove_btn = ttk.Button(
            course_frame,
            text="Remove",
            command=lambda f=course_frame: self._remove_course_row(f)
        )
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.course_rows.append((course_frame, name_entry, marks_entry, credits_combo))

    def _remove_course_row(self, frame):
        if len(self.course_rows) > 1:  # Keep at least one row
            idx = next(i for i, (f, _, _, _) in enumerate(self.course_rows) if f == frame)
            self.course_rows.pop(idx)
            frame.destroy()
            self._repack_courses()

    def _repack_courses(self):
        for i, (frame, _, _, _) in enumerate(self.course_rows, 1):
            frame.grid(row=i, column=0, columnspan=4, pady=5, sticky='ew')

    def _create_buttons_frame(self):
        buttons_frame = ttk.Frame(self.main_container)
        buttons_frame.pack(fill='x', pady=(0, 20))
        
        # Add Course button
        ttk.Button(
            buttons_frame,
            text="Add Course",
            command=self._add_course_row
        ).pack(side=tk.LEFT, padx=5)
        
        # Calculate button with distinct styling
        calculate_btn = ttk.Button(
            buttons_frame,
            text="Calculate GPA",
            command=self._calculate_and_show_results,
            style='Accent.TButton'
        )
        calculate_btn.pack(side=tk.RIGHT, padx=5)

    def _validate_inputs(self) -> bool:
        # Validate student information
        for key, entry in self.student_entries.items():
            if not entry.get():
                messagebox.showerror(
                    "Error", 
                    f"Please enter {key.replace('_', ' ').title()}"
                )
                return False
        
        # Validate course information
        for _, name_entry, marks_entry, credits_combo in self.course_rows:
            if not name_entry.get():
                messagebox.showerror("Error", "Please enter course name")
                return False
                
            try:
                marks = float(marks_entry.get())
                if not (0 <= marks <= 100):
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Marks should be between 0-100"
                )
                return False
                
            if not credits_combo.get():
                messagebox.showerror(
                    "Error",
                    "Please select credit hours"
                )
                return False
        
        return True

    def _calculate_and_show_results(self):
        if not self._validate_inputs():
            return
            
        # Create student object
        self.student = Student(
            name=self.student_entries["name"].get(),
            father_name=self.student_entries["father_name"].get(),
            enrollment=self.student_entries["enrollment"].get(),
            roll_no=int(self.student_entries["roll_no"].get()),
            degree=self.student_entries["degree"].get()
        )
        
        # Calculate GPA
        total_quality_points = 0
        total_credit_hours = 0
        
        courses = []
        for _, name_entry, marks_entry, credits_combo in self.course_rows:
            course = Course(
                name=name_entry.get(),
                marks=float(marks_entry.get()),
                credit_hours=int(credits_combo.get())
            )
            courses.append(course)
            
            total_quality_points += course.grade_points * course.credit_hours
            total_credit_hours += course.credit_hours
        
        gpa = total_quality_points / total_credit_hours
        
        # Show results
        self._show_results_window(courses, gpa, total_credit_hours)

    def _show_results_window(self, courses: List[Course], gpa: float, total_credit_hours: int):
        results = tk.Toplevel(self)
        results.title("GPA Results")
        results.geometry("800x600")
        
        # Apply the same theme
        results.style = ttkthemes.ThemedStyle(results)
        results.style.set_theme("arc")
        
        main_frame = ttk.Frame(results, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student information
        ttk.Label(
            main_frame,
            text="Student Information",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=(0, 10))
        
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x')
        
        student_info = [
            f"Name: {self.student.name}",
            f"Father's Name: {self.student.father_name}",
            f"Enrollment: {self.student.enrollment}",
            f"Roll No: {self.student.roll_no}",
            f"Degree: {self.student.degree}"
        ]
        
        for info in student_info:
            ttk.Label(
                info_frame, 
                text=info,
                font=('Helvetica', 10)
            ).pack(anchor='w')
        
        # Course information
        ttk.Label(
            main_frame,
            text="Course Details",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=(20, 10))
        
        # Create treeview for course details
        columns = ("Course", "Marks", "Grade", "Credit Hours", "Quality Points")
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Add course data
        for course in courses:
            tree.insert(
                '',
                'end',
                values=(
                    course.name,
                    f"{course.marks:.1f}",
                    course.grade,
                    course.credit_hours,
                    f"{course.grade_points * course.credit_hours:.2f}"
                )
            )
        
        tree.pack(fill='x', pady=10)
        
        # Final GPA
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill='x', pady=20)
        
        ttk.Label(
            result_frame, 
            text=f"Semester GPA: {gpa:.2f}",
            font=('Helvetica', 20, 'bold')
        ).pack()
        
        ttk.Label(
            result_frame,
            text=f"Total Credit Hours: {total_credit_hours}",
            font=('Helvetica', 14)
        ).pack()

if __name__ == "__main__":
    app = GPACalculator()
    app.mainloop()