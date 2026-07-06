from addBook import *
from viewBook import *
from searchBook import *
from issue import *
from delete import *
from returnbook import *
from tkinter import *
from tkinter import Canvas, messagebox
from PIL import ImageTk, Image
import base64
import io
import pymysql

# Database connection
con = pymysql.connect(host="localhost", user="root", password="harinee@11", database="db")
cur = con.cursor()

# Designing the window
root = Tk()
windowWidth = 800
windowHeight = 600
root.geometry(f"{windowWidth}x{windowHeight}")

with open("src/library.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read())

# Decode the base64 image and convert it to an Image object
image_data = base64.b64decode(encoded_image)
stream = io.BytesIO(image_data)
bg = Image.open(stream)

def resize_image(event):
    width = event.width
    height = event.height
    image = bg.resize((width, height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    event.widget.create_image(0, 0, image=photo, anchor='nw')
    event.widget.image = photo

def create_canvas(root):
    canvas = Canvas(root, width=windowWidth, height=windowHeight)
    canvas.pack(fill="both", expand=True)
    canvas.bind('<Configure>', resize_image)
    initial_image = bg.resize((windowWidth, windowHeight), Image.LANCZOS)
    initial_photo = ImageTk.PhotoImage(initial_image)
    canvas.create_image(0, 0, image=initial_photo, anchor='nw')
    canvas.image = initial_photo
    return canvas

# Login page
def login_page():
    for widget in root.winfo_children():
        widget.destroy()

    canvas = create_canvas(root)

    login_frame = Frame(root, bg="white", bd=5)
    login_frame.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.4)

    Label(login_frame, text="Username:", bg='white').place(relx=0.1, rely=0.2)
    username_entry = Entry(login_frame)
    username_entry.place(relx=0.4, rely=0.2, relwidth=0.5)

    Label(login_frame, text="Password:", bg='white').place(relx=0.1, rely=0.4)
    password_entry = Entry(login_frame, show="*")
    password_entry.place(relx=0.4, rely=0.4, relwidth=0.5)

    Button(login_frame, text="Login", bg='black', fg='white', command=lambda: login(username_entry.get(), password_entry.get())).place(relx=0.3, rely=0.6, relwidth=0.4)
    Button(login_frame, text="Sign Up", bg='black', fg='white', command=signup_page).place(relx=0.3, rely=0.75, relwidth=0.4)
    Button(login_frame, text="Forgot Password", bg='black', fg='white', command=forgot_password_page).place(relx=0.3, rely=0.9, relwidth=0.4)

# Signup page
def signup_page():
    for widget in root.winfo_children():
        widget.destroy()

    canvas = create_canvas(root)

    signup_frame = Frame(root, bg="white", bd=5)
    signup_frame.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.6)

    Label(signup_frame, text="Username:", bg='white').place(relx=0.1, rely=0.1)
    username_entry = Entry(signup_frame)
    username_entry.place(relx=0.4, rely=0.1, relwidth=0.5)

    Label(signup_frame, text="Password:", bg='white').place(relx=0.1, rely=0.25)
    password_entry = Entry(signup_frame, show="*")
    password_entry.place(relx=0.4, rely=0.25, relwidth=0.5)

    Label(signup_frame, text="Email:", bg='white').place(relx=0.1, rely=0.4)
    email_entry = Entry(signup_frame)
    email_entry.place(relx=0.4, rely=0.4, relwidth=0.5)

    Label(signup_frame, text="Enter your favourite teacher:", bg='white').place(relx=0.1, rely=0.55)
    secret_key_entry = Entry(signup_frame)
    secret_key_entry.place(relx=0.4, rely=0.55, relwidth=0.5)

    Button(signup_frame, text="Sign Up", bg='black', fg='white', command=lambda: signup(username_entry.get(), password_entry.get(), email_entry.get(), secret_key_entry.get())).place(relx=0.3, rely=0.75, relwidth=0.4)
    Button(signup_frame, text="Back to Login", bg='black', fg='white', command=login_page).place(relx=0.3, rely=0.85, relwidth=0.4)

# Login function
def login(username, password):
    query = f"SELECT * FROM users WHERE username=%s AND password=%s"
    cur.execute(query, (username, password))
    result = cur.fetchone()
    if result:
        main_page(username)
    else:
        messagebox.showerror("Error", "Invalid credentials")

# Signup function
def signup(username, password, email, secret_key):
    query = f"INSERT INTO users (username, password, email, secret_key) VALUES (%s, %s, %s, %s)"
    try:
        cur.execute(query, (username, password, email, secret_key))
        con.commit()
        messagebox.showinfo("Success", "Account created successfully")
        login_page()
    except pymysql.MySQLError as e:
        messagebox.showerror("Error", f"Error: {e}")

# Forgot password page
def forgot_password_page():
    for widget in root.winfo_children():
        widget.destroy()

    canvas = create_canvas(root)

    forgot_password_frame = Frame(root, bg="white", bd=5)
    forgot_password_frame.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.4)

    Label(forgot_password_frame, text="Email:", bg='white').place(relx=0.1, rely=0.2)
    email_entry = Entry(forgot_password_frame)
    email_entry.place(relx=0.4, rely=0.2, relwidth=0.5)

    Label(forgot_password_frame, text="Secret Key:", bg='white').place(relx=0.1, rely=0.4)
    secret_key_entry = Entry(forgot_password_frame)
    secret_key_entry.place(relx=0.4, rely=0.4, relwidth=0.5)

    Button(forgot_password_frame, text="Submit", bg='black', fg='white', command=lambda: verify_secret_key(email_entry.get(), secret_key_entry.get())).place(relx=0.3, rely=0.7, relwidth=0.4)
    Button(forgot_password_frame, text="Back to Login", bg='black', fg='white', command=login_page).place(relx=0.3, rely=0.85, relwidth=0.4)

# Verify secret key function
def verify_secret_key(email, secret_key):
    query = f"SELECT * FROM users WHERE email=%s AND secret_key=%s"
    cur.execute(query, (email, secret_key))
    result = cur.fetchone()
    if result:
        reset_password_page(email)
    else:
        messagebox.showerror("Error", "Invalid email or secret key")

# Reset password page
def reset_password_page(email):
    for widget in root.winfo_children():
        widget.destroy()

    canvas = create_canvas(root)

    reset_password_frame = Frame(root, bg="white", bd=5)
    reset_password_frame.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.4)

    Label(reset_password_frame, text="New Password:", bg='white').place(relx=0.1, rely=0.4)
    new_password_entry = Entry(reset_password_frame, show="*")
    new_password_entry.place(relx=0.4, rely=0.4, relwidth=0.5)

    Button(reset_password_frame, text="Reset Password", bg='black', fg='white', command=lambda: reset_password(email, new_password_entry.get())).place(relx=0.3, rely=0.7, relwidth=0.4)
    Button(reset_password_frame, text="Back to Login", bg='black', fg='white', command=login_page).place(relx=0.3, rely=0.85, relwidth=0.4)

# Reset password function
def reset_password(email, new_password):
    query = f"UPDATE users SET password=%s WHERE email=%s"
    try:
        cur.execute(query, (new_password, email))
        con.commit()
        messagebox.showinfo("Success", "Password reset successfully")
        login_page()
    except pymysql.MySQLError as e:
        messagebox.showerror("Error", f"Error: {e}")

# Main page after login
def main_page(username):
    for widget in root.winfo_children():
        widget.destroy()

    canvas = create_canvas(root)

    head = Frame(root, bg="yellow", bd=5)
    head.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
    headLabel = Label(head, text=f"Welcome to the Library, {username}", bg='black', fg='white', font=('Arial Black', 20))
    headLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Adding the buttons
    Button(root, text="Add Book", bg='black', activebackground='#e7e7e7', fg='white', font=('Arial Black', 16), command=addBook).place(relx=0.28, rely=0.4, relwidth=0.45, relheight=0.1)
    Button(root, text="Delete Book", bg='black', activebackground='#e7e7e7', fg='white', font=('Arial Black', 16), command=delete).place(relx=0.28, rely=0.5, relwidth=0.45, relheight=0.1)
    Button(root, text="View Books", bg='black', activebackground='#e7e7e7', fg='white', font=('Arial Black', 16), command=View).place(relx=0.28, rely=0.6, relwidth=0.45, relheight=0.1)
    Button(root, text="Issue Book", bg='black', activebackground='#e7e7e7', fg='white', font=('Arial Black', 16), command=issue).place(relx=0.28, rely=0.7, relwidth=0.45, relheight=0.1)
    Button(root, text="Return Book", bg='black', activebackground='#e7e7e7', fg='white', font=('Arial Black', 16), command=returnBook).place(relx=0.28, rely=0.8, relwidth=0.45, relheight=0.1)
    Button(root, text="Search Book", bg='black', activebackground='#e7e7e7', fg='white', font=('Arial Black', 16), command=searchBook).place(relx=0.28, rely=0.9, relwidth=0.45, relheight=0.1)
    Button(root, text="Logout", bg='black', fg='white',font=('Arial Black', 16), command=login_page).place(relx=0.8, rely=0.05, relwidth=0.15, relheight=0.05)

# Start the application with the login page
login_page()
root.mainloop()
