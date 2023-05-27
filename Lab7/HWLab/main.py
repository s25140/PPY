import tkinter as tk
from tkinter import ttk
import mysql.connector


root = tk.Tk()

def connectToDatabase(autoCommit = False):
    cnx = mysql.connector.connect(
        host="db4free.net",
        user="s25140",
        password="",
        database="ppy25140"
     )
    cnx.autocommit = autoCommit
    return cnx

def insertGrade(grades, studentID): #grades = [(subj,grade),(),..]
    cnx = None
    cursor = None
    try:
        cnx = connectToDatabase()
        cursor = cnx.cursor()
        for gradeInfo in grades:
            cursor.execute("SELECT ID FROM Subjects WHERE Name = %s", (gradeInfo[0],))
            SubjID = cursor.fetchall()[0][0]
            cursor.execute("INSERT INTO Students_Subjects VALUES(%s, %s ,%s);", (studentID,SubjID,gradeInfo[1]))
        cnx.commit()
    except Exception as e:
        print(e)
    finally:
        if cnx:
            cnx.close()
        if cursor:
            cursor.close()

def addStudentWindow():
    new_window = tk.Toplevel(root)
    new_window.title("Dodaj nowego studenta")
    fName_label = ttk.Label(new_window, text="Imię:")
    fName_label.pack()
    fName_entry = ttk.Entry(new_window)
    fName_entry.pack()
    lName_label = ttk.Label(new_window, text="Nazwisko:")
    lName_label.pack()
    lName_entry = ttk.Entry(new_window)
    lName_entry.pack()
    index_label = ttk.Label(new_window, text="Numer indeksu:")
    index_label.pack()
    index_entry = ttk.Entry(new_window)
    index_entry.pack()
    frame = tk.Frame(new_window)
    frame.pack()
    GradeList = []
    cnx = connectToDatabase()
    cur = cnx.cursor()
    cur.execute("SELECT Name FROM Subjects;")
    SubjectsList = [name[0] for name in cur.fetchall()]
    cur.close()
    cnx.close()
    def add_grade_UI():
        global grade_counter

        subject_combobox = tk.ttk.Combobox(frame, values=SubjectsList)
        subject_combobox.grid(row=grade_counter, column=0)

        grade_label = tk.Label(frame, text="Grade:")
        grade_label.grid(row=grade_counter, column=1)
        slider = tk.Scale(frame, from_=1, to=6, orient=tk.HORIZONTAL)
        slider.grid(row=grade_counter, column=1)

        GradeList.append([subject_combobox,slider])

        grade_counter += 1

    category_label = ttk.Label(new_window, text="Oceny:")
    category_label.pack()
    add_grade_button = tk.Button(new_window, text="Add Grade", command=add_grade_UI)
    add_grade_button.pack()

    def add_new():
        cursor = None
        cnx = None
        try:
            grades = [(grade[0].get(), int(grade[1].get())) for grade in GradeList]#[(subj,grade),(),..]
            cnx = connectToDatabase(True)
            cursor = cnx.cursor()
            params = (fName_entry.get(), lName_entry.get(), index_entry.get())
            cursor.execute("INSERT INTO Students (FirstName, LastName, NrIndex) VALUES (%s, %s, %s)", params)
            insertGrade(grades, cursor.lastrowid)
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        load_data()
        new_window.destroy()

    add_button = ttk.Button(new_window, text="Dodaj", command=add_new)
    add_button.pack()

button = tk.Button(root, text = "Dodaj nowego studenta", command = addStudentWindow)

treeview = ttk.Treeview(root)
treeview["columns"] = ("id","fName", "lName", "index")
treeview.column("#0", width=0)
treeview.heading("id", text="ID")
treeview.heading("fName", text="FirstName")
treeview.heading("lName", text="LastName")
treeview.heading("index", text="NrIndex")

def load_data():
    cnx = connectToDatabase()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Students;")
    result = cur.fetchall()
    cur.close()
    cnx.close()

    treeview.delete(*treeview.get_children())
    for row in result:
        treeview.insert("","end",values=(row[0],row[1],row[2],row[3]))


grade_counter = 0
load_data()

def open_details_window(event): # Pobranie zaznaczonego elementu
    selected_item = treeview.focus()
    if not selected_item: return
    item_data = treeview.item(selected_item)
    item_values = item_data['values']
    details_window = tk.Toplevel(root)
    details_window.title("Szczegóły")

    # Tworzenie i wyświetlanie widgetów opartych na danych z zaznaczonego elementu
    id_label = ttk.Label(details_window, text="ID:")
    id_label.pack()
    id_entry = ttk.Entry(details_window)
    id_entry.insert(0, item_values[0])
    id_entry.config(state="disabled")  # Uniemożliwienie zmiany id
    id_entry.pack()
    fName_label = ttk.Label(details_window, text="Imię:")
    fName_label.pack()
    fName_entry = ttk.Entry(details_window)
    fName_entry.insert(0, item_values[1])
    fName_entry.pack()
    lName_label = ttk.Label(details_window, text="Autor:")
    lName_label.pack()
    lName_entry = ttk.Entry(details_window)
    lName_entry.insert(0, item_values[2])
    lName_entry.pack()
    index_label = ttk.Label(details_window, text="Nr Indeksu:")
    index_label.pack()
    index_entry = ttk.Entry(details_window)
    index_entry.insert(0, item_values[3])
    index_entry.pack()
    category_label = ttk.Label(details_window, text="Oceny:")
    category_label.pack()
    cnx0 = connectToDatabase()
    cur0 = cnx0.cursor()
    cur0.execute("SELECT Name, Grade, ID_Subject FROM Students_Subjects INNER JOIN Subjects ON ID_Subject = ID "
                "WHERE ID_Student = %s;",(id_entry.get(),))
    grades = cur0.fetchall()
    cur0.execute("SELECT Name FROM Subjects;")
    SubjectsList = [name[0] for name in cur0.fetchall()]
    cur0.close()
    cnx0.close()
    frame = tk.Frame(details_window)
    frame.pack()
    def remove_grade_UI():
        cnx = connectToDatabase(True)
        cur = cnx.cursor()
        cur.execute("DELETE FROM Students_Subjects WHERE ID_Student = %s AND ID_Subject = %s", (id_entry.get(), grade[2]))
        cur.close()
        cnx.close()
        grade_label.config(text=f"{grade[0]} [Removed]")
    i = 0
    for grade in grades:
        grade_label = ttk.Label(frame, text=grade[0])
        grade_label.grid(row=i, column=0)
        grade_entry = ttk.Entry(frame)
        grade_entry.insert(0, grade[1])
        grade_entry.config(state="disabled")  # Uniemożliwienie zmiany id
        grade_entry.grid(row=i, column=1)
        delete_grade_button = tk.Button(frame, text="Remove Grade", command=remove_grade_UI)
        delete_grade_button.grid(row=i, column=2)
        i+=1
    GradeList = []
    def add_grade_UI():
        global grade_counter

        subject_combobox = tk.ttk.Combobox(frame, values=SubjectsList)
        subject_combobox.grid(row=grade_counter, column=0)

        grade_label = tk.Label(frame, text="Grade:")
        grade_label.grid(row=grade_counter, column=1)
        slider = tk.Scale(frame, from_=1, to=6, orient=tk.HORIZONTAL)
        slider.grid(row=grade_counter, column=1)

        GradeList.append([subject_combobox,slider])

        grade_counter += 1

    add_grade_button = tk.Button(details_window, text="Add Grade", command=add_grade_UI)
    add_grade_button.pack()
    def update():
        cnx = connectToDatabase()
        cur = cnx.cursor()
        sql = "UPDATE Students SET FirstName=%s, LastName=%s, NrIndex=%s WHERE id=%s"
        params = (fName_entry.get(), lName_entry.get(), index_entry.get(), id_entry.get())
        cur.execute(sql, params)
        cnx.commit()
        cur.close()
        cnx.close()
        gradesList = [(grade[0].get(), int(grade[1].get())) for grade in GradeList]#[(subj,grade),(),..]
        insertGrade(gradesList, id_entry.get())
        load_data()
        details_window.destroy()
    def delete():
        cnx = connectToDatabase()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM Students_Subjects WHERE ID_Student = %s",(id_entry.get(),))
        sql = "DELETE FROM Students WHERE id = %s"
        params = (id_entry.get(),)
        cursor.execute(sql, params)
        cnx.commit()
        cursor.close()
        cnx.close()
        load_data()
        details_window.destroy()

    updateButton = ttk.Button(details_window, text="Aktualizuj", command=update)
    updateButton.pack()
    deleteButton = ttk.Button(details_window, text="Usuń", command=delete)
    deleteButton.pack()


treeview.bind("<Double-1>",open_details_window)
treeview.pack()
button.pack()

root.mainloop()

