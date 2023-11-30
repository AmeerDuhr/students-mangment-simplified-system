import PySimpleGUI as sg
import sqlite3

# Constants
DATABASE_PATH = "./database.db"

# Student Class
class Student:
    def __init__(self, id, first, last, phone, major):
        self.id = id
        self.first = first
        self.last = last
        self.phone = phone
        self.major = major

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.id == other.id and self.first == other.first and self.last == other.last and self.phone == other.phone and self.major == other.major
        return False
    
    def __repr__(self) -> str:
        return f"{self.id}. {self.first} {self.last} ({self.phone}) - {self.major}"

# CRUD Operations
def init_database():
    with sqlite3.connect(DATABASE_PATH) as db:
        cr = db.cursor()
        cr.execute('''
            CREATE TABLE if not exists "students" (
            "id"	INTEGER NOT NULL,
            "first"	TEXT,
            "last"	TEXT,
            "phone"	TEXT,
            "major"	TEXT,
            PRIMARY KEY("id"));
            ''')
        db.commit()

def get_all(search_text):
    students = []
    init_database()
    with sqlite3.connect(DATABASE_PATH) as db:
        cr = db.cursor()
        cr.execute(f"SELECT * FROM students WHERE (id LIKE '%{search_text}%' OR first LIKE '%{search_text}%' OR last LIKE '%{search_text}%' OR phone LIKE '%{search_text}%' OR major LIKE '%{search_text}%');")
        students = cr.fetchall()
    return students

def add(student: Student):
    init_database()
    with sqlite3.connect(DATABASE_PATH) as db:
        cr = db.cursor()
        cr.execute(f'INSERT INTO students (id, first, last, phone, major) VALUES ({student.id}, "{student.first}", "{student.last}", "{student.phone}", "{student.major}");')
    db.commit()
def edit(student: Student, id: int):
    init_database()
    with sqlite3.connect(DATABASE_PATH) as db:
        cr = db.cursor()
        cr.execute(f'UPDATE students SET id={student.id}, first="{student.first}", last="{student.last}", phone="{student.phone}", major="{student.major}" WHERE id={id};')
    db.commit()
def delete(id):
    init_database()
    with sqlite3.connect(DATABASE_PATH) as db:
        cr = db.cursor()
        cr.execute(f'DELETE FROM students WHERE id={id};')
        db.commit()

# Helping Functions
def set_inputs(student: Student):
    window['id_input'].update(value=student.id)
    window['first_input'].update(value=student.first)
    window['last_input'].update(value=student.last)
    window['phone_input'].update(value=student.phone)
    window['major_input'].update(value=student.major)

def clear_inputs():
    set_inputs(Student("", "", "", "", ""))

def get_selected_student() -> Student:
    if len(values['students_table']) != 0:
        return Student(*(window["students_table"].get()[values["students_table"][0]]))

def get_student_inputs() -> Student:
    return Student(
        window['id_input'].get(),
        window['first_input'].get(),
        window['last_input'].get(),
        window['phone_input'].get(),
        window['major_input'].get()
    )

def update_students_table():
    window['students_table'].update(get_all(values['search_input']))

# PySimpleGUI Window
sg.set_options(font=("Arial", 16))
sg.theme("DefaultNoMoreNagging")

crud_layout = [
    [sg.Button("Add", key="add_button", expand_x=True)],
    [sg.Button("Edit", key="edit_button", expand_x=True)],
    [sg.Button("Delete", key="delete_button", expand_x=True)],
    [sg.Button("Clear", key="clear_button", expand_x=True)],
    [sg.Text("Id:", size=12), sg.Input(key="id_input", size=32, expand_x=True)],
    [sg.Text("FirstName:", size=12), sg.Input(key="first_input", size=32, expand_x=True)],
    [sg.Text("LastName:", size=12), sg.Input(key="last_input", size=32, expand_x=True)],
    [sg.Text("PhoneNumber:", size=12), sg.Input(key="phone_input", size=32, expand_x=True)],
    [sg.Text("Major:", size=12), sg.Input(key="major_input", size=32, expand_x=True)],
]

main_layout = [
    [sg.Text('Search:'),
     sg.Input(key='search_input', expand_x=True),
     sg.Button("Search", key="search_button")],
    [sg.Table(values=[], headings=["Id", "FirstName", "LastName", "PhoneNumber", "Major"],
              key="students_table", auto_size_columns=True, justification='c',
              expand_x=True, expand_y=True, enable_events=True)]
]

layout = [
    [sg.Column(main_layout, expand_y=True, expand_x=True),
     sg.Column(crud_layout, expand_y=True, expand_x=True)]
]

window = sg.Window("Students Mangement System", layout,
                   margins=(10, 10), size=(1150, 550),
                   element_justification='c', resizable=True, finalize=True)

while True:
    event, values = window.read()
    if event in ("Exit", sg.WIN_CLOSED): break
    elif event == "search_button": update_students_table()
    elif event == "students_table":
        if len(values['students_table']) != 0:
            set_inputs(get_selected_student())
    elif event == "clear_button": clear_inputs()
    elif event == "add_button":
        try:
            add(get_student_inputs())
            clear_inputs()
            update_students_table()
        except:
            sg.popup("An error occured. Did you perhabs forget the Id?")
    elif event == "edit_button":
        try:
            edit(get_student_inputs(), get_selected_student().id)
            clear_inputs()
            update_students_table()
        except:
            sg.popup("No selected students.")
    elif event == "delete_button":
        try:
            delete(get_selected_student().id)
            clear_inputs()
            update_students_table()
        except:
            sg.popup("No selected students.")

window.close()

