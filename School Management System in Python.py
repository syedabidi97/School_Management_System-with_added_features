import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

# Use a consistent color scheme
PRIMARY_COLOR = '#3498db'  # Blue
SECONDARY_COLOR = '#e74c3c'  # Red
BACKGROUND_COLOR = '#ecf0f1'  # Light Gray
TEXT_COLOR = '#2c3e50'  # Dark Gray

# Fonts
HEAD_LABEL_FONT = ("Noto Sans CJK TC", 15, 'bold')
LABEL_FONT = ('Garamond', 12)
ENTRY_FONT = ('Garamond', 11)

# Database Connection
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()

connector.execute(
    "CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)"
)

# Create a new table for attendance
connector.execute(
    "CREATE TABLE IF NOT EXISTS ATTENDANCE (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, STUDENT_ID INTEGER, DATE TEXT, STATUS TEXT)"
)

# Create a new table for courses
connector.execute(
    "CREATE TABLE IF NOT EXISTS COURSES (COURSE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, DESCRIPTION TEXT)"
)


def reset_fields():
    name_strvar.set('')
    email_strvar.set('')
    contact_strvar.set('')
    gender_strvar.set('')
    dob.set_date(datetime.datetime.now().date())
    stream_strvar.set('')


def reset_form():
    tree.delete(*tree.get_children())
    reset_fields()


def display_records():
    tree.delete(*tree.get_children())
    curr = cursor.execute('SELECT * FROM SCHOOL_MANAGEMENT')
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)


def add_record():
    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    stream = stream_strvar.get()
    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            cursor.execute(
                'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)',
                (name, email, contact, gender, DOB, stream)
            )
            connector.commit()
            mb.showinfo('Record added', f"Record of {name} was successfully added")
            reset_fields()
            display_records()
        except Exception as e:
            mb.showerror('Error', f'An error occurred: {e}')


def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        tree.delete(current_item)
        cursor.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()
        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
        display_records()


def view_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select a record to view')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        name_strvar.set(selection[1])
        email_strvar.set(selection[2])
        contact_strvar.set(selection[3])
        gender_strvar.set(selection[4])
        date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))
        dob.set_date(date)
        stream_strvar.set(selection[6])


def mark_attendance():
    if not tree.selection():
        mb.showerror('Error!', 'Please select a student from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        student_id = values["values"][0]
        date_today = datetime.datetime.now().strftime("%Y-%m-%d")
        status = "Present"  # You can customize this based on your needs

        cursor.execute(
            'INSERT INTO ATTENDANCE (STUDENT_ID, DATE, STATUS) VALUES (?,?,?)',
            (student_id, date_today, status)
        )
        connector.commit()
        mb.showinfo('Attendance Marked', f"Attendance for Student ID {student_id} marked as {status}")


def reset_course_fields():
    course_name_strvar.set('')
    course_description_strvar.set('')


def add_course():
    course_name = course_name_strvar.get()
    course_description = course_description_strvar.get()

    if not course_name or not course_description:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            cursor.execute(
                'INSERT INTO COURSES (NAME, DESCRIPTION) VALUES (?, ?)',
                (course_name, course_description)
            )
            connector.commit()
            mb.showinfo('Course added', f"Course {course_name} was successfully added")
            reset_course_fields()
            display_courses()
        except Exception as e:
            mb.showerror('Error', f'An error occurred while adding the course: {e}')


def open_signup_window():
    signup_window = Toplevel(main)
    signup_window.title('Signup')
    signup_window.geometry('300x200')

    Label(signup_window, text="Username:", font=LABEL_FONT).pack(pady=5)
    new_username_entry = Entry(signup_window, font=ENTRY_FONT)
    new_username_entry.pack(pady=5)

    Label(signup_window, text="Password:", font=LABEL_FONT).pack(pady=5)
    new_password_entry = Entry(signup_window, show='*', font=ENTRY_FONT)
    new_password_entry.pack(pady=5)

    Button(signup_window, text='Signup', command=signup, font=LABEL_FONT, bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).pack(pady=10)


def open_login_window():
    login_window = Toplevel(main)
    login_window.title('Login')
    login_window.geometry('300x200')

    Label(login_window, text="Username:", font=LABEL_FONT).pack(pady=5)
    username_entry = Entry(login_window, font=ENTRY_FONT)
    username_entry.pack(pady=5)

    Label(login_window, text="Password:", font=LABEL_FONT).pack(pady=5)
    password_entry = Entry(login_window, show='*', font=ENTRY_FONT)
    password_entry.pack(pady=5)

    Button(login_window, text='Login', command=login, font=LABEL_FONT, bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).pack(pady=10)


def display_courses():
    courses_window = Toplevel(main)
    courses_window.title('Courses')

    tree_courses = ttk.Treeview(courses_window, height=10, selectmode=BROWSE,
                                columns=('Course ID', 'Name', 'Description'))

    tree_courses.heading('Course ID', text='ID', anchor=CENTER)
    tree_courses.heading('Name', text='Name', anchor=CENTER)
    tree_courses.heading('Description', text='Description', anchor=CENTER)

    tree_courses.column('#0', width=0, stretch=NO)
    tree_courses.column('#1', width=40, stretch=NO)
    tree_courses.column('#2', width=140, stretch=NO)
    tree_courses.column('#3', width=200, stretch=NO)

    tree_courses.pack()

    curr_courses = cursor.execute('SELECT * FROM COURSES')
    data_courses = curr_courses.fetchall()
    for records in data_courses:
        tree_courses.insert('', END, values=records)


# GUI Configuration
main = Tk()
main.title('School Management System')
main.geometry('1000x600')
main.resizable(0, 0)
main.attributes('-alpha', True)
main.config(bg=BACKGROUND_COLOR)

# Frames Configuration
left_frame = Frame(main, bg=PRIMARY_COLOR)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)
center_frame = Frame(main, bg=SECONDARY_COLOR)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
right_frame = Frame(main, bg=BACKGROUND_COLOR)
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
stream_strvar = StringVar()

course_name_strvar = StringVar()  # Add this line for course registration
course_description_strvar = StringVar()

# Labels Configuration
Label(main, text="SCHOOL MANAGEMENT SYSTEM", font=HEAD_LABEL_FONT, bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).pack(
    side=TOP, fill=X)


# Entry and Label Configuration
Label(left_frame, text="Name:", font=LABEL_FONT).place(x=20, rely=0.05)
Label(left_frame, text="Contact No:", font=LABEL_FONT).place(x=20, rely=0.15)
Label(left_frame, text="Email Address:", font=LABEL_FONT).place(x=20, rely=0.25)
Label(left_frame, text="Gender:", font=LABEL_FONT).place(x=20, rely=0.35)
Label(left_frame, text="Date:", font=LABEL_FONT).place(x=20, rely=0.45)
Label(left_frame, text="Type Any Letter For Confirmation", font=LABEL_FONT).place(x=20, rely=0.55)
Entry(left_frame, width=19, textvariable=name_strvar, font=ENTRY_FONT, bg=BACKGROUND_COLOR).place(x=20, rely=0.10)

# Entry and Label Configuration
Entry(left_frame, width=19, textvariable=name_strvar, font=ENTRY_FONT, bg=BACKGROUND_COLOR).place(x=20, rely=0.10)
Entry(left_frame, width=19, textvariable=contact_strvar, font=ENTRY_FONT, bg=BACKGROUND_COLOR).place(x=20, rely=0.20)
Entry(left_frame, width=19, textvariable=email_strvar, font=ENTRY_FONT, bg=BACKGROUND_COLOR).place(x=20, rely=0.30)
Entry(left_frame, width=19, textvariable=stream_strvar, font=ENTRY_FONT, bg=BACKGROUND_COLOR).place(x=20, rely=0.60)
OptionMenu(left_frame, gender_strvar, 'Male', 'Female').place(x=20, rely=0.40, relwidth=0.5)
dob = DateEntry(left_frame, font=ENTRY_FONT, width=15, background=BACKGROUND_COLOR)
dob.place(x=20, rely=0.50)


# Entry(center_frame, width=19, textvariable=course_name_strvar, font=ENTRY_FONT, bg=BACKGROUND_COLOR).place(x=20,rely=0.80)
Entry(center_frame, width=19, textvariable=course_description_strvar, font=ENTRY_FONT,
      bg=BACKGROUND_COLOR).place(x=20, rely=0.75)

# ... (rest of the code)

Label(center_frame, text='Course Name:', font=LABEL_FONT).place(x=20, rely=0.60)
Label(center_frame, text='Course Description:', font=LABEL_FONT).place(x=20, rely=0.70)
Entry(center_frame, width=19, textvariable=course_name_strvar, font=ENTRY_FONT, bg=BACKGROUND_COLOR).place(x=20, rely=0.65)


# Buttons Configuration
Button(left_frame, text='Submit and Add Record', font=LABEL_FONT, command=add_record, width=18, bg=SECONDARY_COLOR,
       fg=BACKGROUND_COLOR).place(relx=0.025, rely=0.70)

Button(center_frame, text='Delete Record', font=LABEL_FONT, command=remove_record, width=15,
       bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).place(relx=0.1, rely=0.15)
Button(center_frame, text='View Record', font=LABEL_FONT, command=view_record, width=15,
       bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).place(relx=0.1, rely=0.20)
Button(center_frame, text='Reset Fields', font=LABEL_FONT, command=reset_fields, width=15,
       bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).place(relx=0.1, rely=0.25)
Button(center_frame, text='Delete database', font=LABEL_FONT, command=reset_form, width=15,
       bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).place(relx=0.1, rely=0.30)
Button(center_frame, text='Mark Attendance', font=LABEL_FONT, command=mark_attendance, width=15,
       bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).place(relx=0.1, rely=0.35)
Button(center_frame, text='Add Course', font=LABEL_FONT, command=add_course, width=15,
       bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).place(relx=0.1, rely=0.40)

Label(right_frame, text='Students Records', font=HEAD_LABEL_FONT, bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR).pack(
    side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Stream"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)
tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

Button(main, text='Login', font=LABEL_FONT, command=open_login_window, bg=PRIMARY_COLOR,
       fg=BACKGROUND_COLOR).place(x=20, y=30)
Button(main, text='Signup', font=LABEL_FONT, command=open_signup_window, bg=SECONDARY_COLOR,
       fg=BACKGROUND_COLOR).place(x=100, y=30)

main.update()
main.mainloop()
