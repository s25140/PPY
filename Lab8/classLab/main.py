import tkinter as tk
from tkinter import ttk
import mysql.connector

root = tk.Tk()
def connectToDatabase(autoCommit = False):
    cnx = mysql.connector.connect(
        host="db4free.net",
        user="s25140",
        password="Pavel200404",
        database="ppy25140"
     )
    cnx.autocommit = autoCommit
    return cnx

def open_new_book_window():
    new_window = tk.Toplevel(root)
    new_window.title("Dodaj nową książkę")
    title_label = ttk.Label(new_window, text="Tytuł:")
    title_label.pack()
    title_entry = ttk.Entry(new_window)
    title_entry.pack()
    author_label = ttk.Label(new_window, text="Autor:")
    author_label.pack()
    author_entry = ttk.Entry(new_window)
    author_entry.pack()
    price_label = ttk.Label(new_window, text="Cena:")
    price_label.pack()
    price_entry = ttk.Entry(new_window)
    price_entry.pack()
    category_label = ttk.Label(new_window, text="Kategoria:")
    category_label.pack()
    category_entry = ttk.Entry(new_window)
    category_entry.pack()
    def add_new():
        new_title = title_entry.get()
        new_author = author_entry.get()
        new_price = price_entry.get()
        new_category = category_entry.get()
        try:
            cnx = connectToDatabase()
            cursor = cnx.cursor()

            sql = "INSERT INTO books (title, author, price, category) VALUES (%s, %s, %s, %s)"
            params = (new_title, new_author, new_price, new_category)
            cursor.execute(sql, params)
            cnx.commit()  # Zapisanie zmian w bazie
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()  # Zamknięcie kursora
            if cnx:
                cnx.close()

        load_data()
        new_window.destroy()

    add_button = ttk.Button(new_window, text="Dodaj", command=add_new)
    add_button.pack()

button = tk.Button(root, text = "Dodaj książkę", command = open_new_book_window)

treeview = ttk.Treeview(root)
treeview["columns"] = ("id", "title", "author", "price", "category")
treeview.column("#0", width=0)
treeview.heading("id", text="ID")
treeview.heading("title", text="Tytuł")
treeview.heading("author", text="Autor")
treeview.heading("price", text="Cena")
treeview.heading("category", text="Kategoria")

def load_data():
    cnx = connectToDatabase()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM books")
    result = cur.fetchall()
    cur.close()
    cnx.close()

    treeview.delete(*treeview.get_children())
    for row in result:
        treeview.insert("","end",values=(row[0],row[1],row[2],row[3],row[4]))

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
    title_label = ttk.Label(details_window, text="Tytuł:")
    title_label.pack()
    title_entry = ttk.Entry(details_window)
    title_entry.insert(0, item_values[1])
    title_entry.pack()
    author_label = ttk.Label(details_window, text="Autor:")
    author_label.pack()
    author_entry = ttk.Entry(details_window)
    author_entry.insert(0, item_values[2])
    author_entry.pack()
    price_label = ttk.Label(details_window, text="Cena:")
    price_label.pack()
    price_entry = ttk.Entry(details_window)
    price_entry.insert(0, item_values[3])
    price_entry.pack()
    category_label = ttk.Label(details_window, text="Kategoria:")
    category_label.pack()
    category_entry = ttk.Entry(details_window)
    category_entry.insert(0, item_values[4])
    category_entry.pack()
    def update():
        cnx = connectToDatabase()
        cur = cnx.cursor()
        sql = "UPDATE books SET title=%s, author=%s, price=%s, category=%s WHERE id=%s"
        params = (title_entry.get(), author_entry.get(), price_entry.get(), category_entry.get(), id_entry.get())
        cur.execute(sql, params)
        cnx.commit()
        cur.close()
        cnx.close()
        load_data()
        details_window.destroy()
    def delete():
        cnx = connectToDatabase()
        cursor = cnx.cursor()
        sql = "DELETE FROM books WHERE id = %s"
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