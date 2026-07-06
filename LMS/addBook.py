from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Combobox
import pymysql

# Database connection
con = pymysql.connect(
    host="localhost",
    user="root",
    password="harinee@11",
    database="db"
)

def RegisterBook():
    cur = con.cursor()
    bid = bookInfo1.get()
    title = bookInfo2.get()
    author = bookInfo3.get()
    status = "Available"
    status = status.lower()
    number_of_books = 1  # Default to 1 for new books

    print(f"Book Type Selected in RegisterBook: {book_type.get()}")  # Debug print

    if bid == "" or title == "" or author == "":
        messagebox.showinfo("Error", "All fields are required")
        return

    if book_type.get() == "New":
        # Insert a new book
        insert_query = f"INSERT INTO {bookTable} (bid, title, author, status, number_of_books) VALUES (%s, %s, %s, %s, %s)"
        try:
            cur.execute(insert_query, (bid, title, author, status, number_of_books))
            con.commit()
            messagebox.showinfo("Success", "New book added to database successfully")
        except Exception as e:
            print(e)  # Debug print
            messagebox.showinfo("Error", "Can't add the new book to database")
    else:
        # Check if the book already exists
        query = f"SELECT * FROM {bookTable} WHERE bid = %s"
        cur.execute(query, (bid,))
        result = cur.fetchone()
        if result:
            # Increment the number of books
            update_query = f"UPDATE {bookTable} SET number_of_books = number_of_books + 1 WHERE bid = %s"
            try:
                cur.execute(update_query, (bid,))
                con.commit()
                messagebox.showinfo("Success", "Existing book quantity incremented successfully")
            except Exception as e:
                print(e)  # Debug print
                messagebox.showinfo("Error", "Failed to update the book quantity")
        else:
            messagebox.showinfo("Error", "Book ID does not exist. Please register as a new book.")

    root.destroy()

def addBook():
    global bookInfo1, bookInfo2, bookInfo3, bookTable, root, book_type

    root = Tk()
    root.title("Add Books")
    root.minsize(width=400, height=400)
    root.geometry("1020x735")

    bookTable = "books"

    Canvas1 = Canvas(root)
    Canvas1.config(bg="Green")
    Canvas1.pack(fill="both", expand=True)

    headingFrame1 = Frame(root, bg="Yellow", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add Books", bg='black', fg='white', font=('Courier New', 20))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    lb1 = Label(labelFrame, text='Book ID:', bg='black', fg='white')
    lb1.place(relx=0.05, rely=0.1, relheight=0.08)

    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.1, relwidth=0.62, relheight=0.08)

    lb2 = Label(labelFrame, text="Title : ", bg='black', fg='white')
    lb2.place(relx=0.05, rely=0.25, relheight=0.08)

    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx=0.3, rely=0.25, relwidth=0.62, relheight=0.08)
    
    lb3 = Label(labelFrame, text="Author : ", bg='black', fg='white')
    lb3.place(relx=0.05, rely=0.4, relheight=0.08)

    bookInfo3 = Entry(labelFrame)
    bookInfo3.place(relx=0.3, rely=0.4, relwidth=0.62, relheight=0.08)

    # Book Type (New or Existing)
    book_type = StringVar()
    book_type.set("existing")  # Set default to "New"

    lb4 = Label(labelFrame, text="Book Type : ", bg='black', fg='white')
    lb4.place(relx=0.05, rely=0.55, relheight=0.08)

    book_type_combobox = ttk.Combobox(labelFrame, textvariable=book_type, state='readonly')
    book_type_combobox['values'] = ('New', 'Existing')
    book_type_combobox.place(relx=0.3, rely=0.55, relwidth=0.62, relheight=0.08)
    book_type_combobox.current(0)  # Set default to "New"

    # Submit Button
    SubmitBtn = Button(root, text="SUBMIT", bg='black', fg='white', font=('Courier New', 11), command=RegisterBook)
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="QUIT", bg='black', fg='white', font=('Courier New', 11), command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()

# Call addBook to test the implementation
#addBook()
