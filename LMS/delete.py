from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import mysql.connector as ms
import pymysql
issueTable = "books_issued"
bookTable = "books"  # Book Table
con = pymysql.connect(
    host="localhost",
    user="root",
    password="harinee@11",
    database="db"
)
cur = con.cursor()

def deleteBook():
    bid = bookInfo1.get()
    
    # Check the current number of books
    checkSql = f"SELECT number_of_books FROM {bookTable} WHERE bid = '{bid}'"
    cur.execute(checkSql)
    result = cur.fetchone()
    
    if result:
        number_of_books = result[0]
        if number_of_books > 1:
            # Decrement the number of books
            updateSql = f"UPDATE {bookTable} SET number_of_books = number_of_books - 1 WHERE bid = '{bid}'"
            try:
                cur.execute(updateSql)
                con.commit()
                messagebox.showinfo('Success', f"Book count decremented. Remaining books: {number_of_books - 1}")
            except:
                messagebox.showinfo("Error", "Failed to update the book count")
        else:
            # Delete the book record
            deleteSql = f"DELETE FROM {bookTable} WHERE bid = '{bid}'"
            deleteIssue = f"DELETE FROM {issueTable} WHERE bid = '{bid}'"
            try:
                cur.execute(deleteSql)
                cur.execute(deleteIssue)
                con.commit()
                messagebox.showinfo('Success', "No more copies of this book. Book record deleted successfully.")
            except:
                messagebox.showinfo("Error", "Can't delete the record")
    else:
        messagebox.showinfo("Error", "Book ID does not exist")
    
    root.destroy()

def delete():
    global bookInfo1, Canvas1, root

    root = Tk()
    root.title("Delete Books")
    root.minsize(width=400, height=400)
    root.geometry("1020x735")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#006B38")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Delete Book", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Book ID to Delete
    lb2 = Label(labelFrame, text="Book ID : ", bg='black', fg='white')
    lb2.place(relx=0.05, rely=0.5)

    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.5, relwidth=0.62)

    # Submit Button
    SubmitBtn = Button(root, text="SUBMIT", bg='black', fg='white', font=('Courier New', 11), command=deleteBook)
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="QUIT", bg='black', fg='white', font=('Courier New', 11), command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()

# Test the delete function
#delete()
