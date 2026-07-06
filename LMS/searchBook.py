from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql

# Database connection
con = pymysql.connect(
    host="localhost",
    user="root",
    password="harinee@11",
    database="db"
)
cur = con.cursor()

def searchBook():
    root = Tk()
    root.title("Search Books")
    root.minsize(width=400, height=400)
    root.geometry("1020x735")

    bookTable = "books"

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#F0F0F0")  # Light grey background for a modern look
    Canvas1.pack(fill="both", expand=True)

    headingFrame1 = Frame(root, bg="#4682B4", bd=5)  # Steel Blue color
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="Search Books", bg='black', fg='white', font=('Arial', 20, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='#DCDCDC')  # Gainsboro background for the form
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    
    lb1 = Label(labelFrame, text='Search by Book ID:', bg='#DCDCDC', fg='black', font=('Arial', 12))
    lb1.place(relx=0.05, rely=0.1, relheight=0.08)

    searchInfo1 = Entry(labelFrame, font=('Arial', 12))
    searchInfo1.place(relx=0.3, rely=0.1, relwidth=0.62, relheight=0.08)

    def search():
        bid = searchInfo1.get()

        query = f"SELECT * FROM {bookTable} WHERE "
        conditions = []
        
        if bid:
            conditions.append(f"bid = '{bid}'")
        
        if conditions:
            query += " AND ".join(conditions)
        else:
            messagebox.showinfo("Error", "Please enter at least one search criterion")
            return

        try:
            cur.execute(query)
            result = cur.fetchall()
            for widget in resultFrame.winfo_children():
                widget.destroy()
            
            if result:
                for i, row in enumerate(result):
                    Label(resultFrame, text=f"{row[0]:<10}{row[1]:<30}{row[2]:<20}{row[3]:<10}{row[4]:<15}{row[5]:<15}", bg='black', fg='white', font=('Arial', 15)).place(relx=0.05, rely=0.1 + i * 0.05)
            else:
                Label(resultFrame, text="No matching records found.", bg='black', fg='white', font=('Arial', 11)).place(relx=0.05, rely=0.1)

        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Failed to fetch results from the database")
        finally:
            cur.close()

    resultFrame = Frame(root, bg='#DCDCDC')
    resultFrame.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.3)

    searchBtn = Button(root, text="SEARCH", bg='#4682B4', fg='white', font=('Arial', 12, 'bold'), command=search)
    searchBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="QUIT", bg='#4682B4', fg='white', font=('Arial', 12, 'bold'), command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()

# Call searchBook to test the implementation
#searchBook()
