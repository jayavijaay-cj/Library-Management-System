from tkinter import *
from tkinter import messagebox
import mysql.connector as sql
import pymysql
# Global variables
page_size = 10  # Number of books per page
current_page = 1  # Current page index

def View():
    # Establish a cursor without the buffered parameter
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="harinee@11",
        database="db"
    )
    cur = con.cursor()

    table = "books"

    root = Tk()
    root.title("View Books")
    root.minsize(width=400, height=400)
    root.geometry("1020x735")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="aqua")
    Canvas1.pack(expand=True, fill="both")

    headingFrame1 = Frame(root, bg="Yellow", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="View Books", bg='black', fg='white', font=('Courier New', 20))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Function to fetch and display books for the current page
    def fetch_books(page_num):
        global current_page
        current_page = page_num
        
        # Clear previous labels in labelFrame
        for widget in labelFrame.winfo_children():
            widget.destroy()

        # Calculate the starting index for the current page
        start_index = (current_page - 1) * page_size

        # SQL query to fetch books for the current page
        getBooks = f"SELECT BID, Title, Author, Status, number_of_books, books_issued FROM {table} LIMIT {page_size} OFFSET {start_index};"

        try:
            cur.execute(getBooks)
            result = cur.fetchall()
            y = 0.25
            for i in result:
                Label(labelFrame, text="%-10s%-30s%-20s%-10s%-15s%-15s" % (i[0], i[1], i[2], i[3], i[4], i[5]), bg='black', fg='white', font=('Courier New', 11)).place(
                    relx=0.05, rely=y)
                y += 0.05
        except sql.Error as e:
            print(f"Error: {e}")
            messagebox.showinfo("Error", "Failed to fetch books from the database")

    # Function to go to the next page
    def next_page():
        global current_page
        current_page += 1
        fetch_books(current_page)

    # Function to go to the previous page
    def prev_page():
        global current_page
        if current_page > 1:
            current_page -= 1
            fetch_books(current_page)

    fetch_books(current_page)  # Initial fetch for the first page

    # Buttons for pagination
    prevBtn = Button(root, text="Previous", bg='black', fg='white', font=('Courier New', 11), command=prev_page)
    prevBtn.place(relx=0.3, rely=0.9, relwidth=0.1, relheight=0.08)

    nextBtn = Button(root, text="Next", bg='black', fg='white', font=('Courier New', 11), command=next_page)
    nextBtn.place(relx=0.6, rely=0.9, relwidth=0.1, relheight=0.08)

    quitBtn = Button(root, text="QUIT", bg='black', fg='white', font=('Courier New', 11), command=root.destroy)
    quitBtn.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()

# Example usage
#View()
