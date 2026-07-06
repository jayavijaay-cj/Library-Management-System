from tkinter import *
from tkinter import messagebox
import mysql_connector as ms

def issueBook():
    cur = ms.con.cursor()
    issueTable = "books_issued"
    bookTable = "books"  # Book Table
    bid = bookInfo1.get()
    sid = bookInfo2.get()
    
    # Check if the book exists and is available
    cur.execute(f"SELECT number_of_books, books_issued FROM {bookTable} WHERE bid = '{bid}'")
    book_info = cur.fetchone()
    
    if not book_info:
        messagebox.showinfo('Error', "Book does not exist")
        return
    
    number_of_books = book_info[0]
    books_issued = book_info[1]

    if books_issued == number_of_books:
        messagebox.showinfo('Error', "No copies of the book are available")
        return

    try:
        # Decrement the number of remaining books
        #remaining_books = number_of_books - 1
        new_books_issued = books_issued + 1
        
        # Update the books table
        status = 'Issued' if new_books_issued == number_of_books  else 'Available'
        update_book = f"UPDATE {bookTable} SET books_issued = {new_books_issued}, status = '{status}' WHERE bid = '{bid}'"
        cur.execute(update_book)
        
        # Update the books_issued table
        insert_issued = f"INSERT INTO {issueTable} (bid, issuedto) VALUES ('{bid}', '{sid}')"
        cur.execute(insert_issued)
        
        ms.con.commit()
        messagebox.showinfo('Success', "Book Issued Successfully")
    except ms.con.Error as e:
        print(f"Error: {e}")
        messagebox.showinfo('Error', "Book Issued Successfully")
    finally:
        cur.close()
        root.destroy()

def issue():
    global bookInfo1, bookInfo2, Canvas1, root

    root = Tk()
    root.title("Issue Books")
    root.minsize(width=400, height=400)
    root.geometry("1020x735")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="magenta")
    Canvas1.pack(expand=True, fill="both")

    headingFrame1 = Frame(root,bg="Yellow",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Issue Books", bg='black', fg='white', font = ('Courier New',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.4)

    lb1=Label(labelFrame,text='Book ID:', bg='black',fg='white')
    lb1.place(relx=0.05, rely=0.2, relheight=0.08)

    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.2, relwidth=0.62, relheight=0.08)

    lb2=Label(labelFrame,text='Student ID:', bg='black',fg='white')
    lb2.place(relx=0.05, rely=0.5, relheight=0.08)

    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx=0.3, rely=0.5, relwidth=0.62, relheight=0.08)

    #Submit Button
    SubmitBtn = Button(root, text="ISSUE", bg='black', fg='white', font=('Courier New', 11), command=issueBook)
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="QUIT", bg='black', fg='white', font=('Courier New', 11), command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()
