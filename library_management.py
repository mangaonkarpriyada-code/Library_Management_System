import tkinter as tk
from tkinter import messagebox
import mysql.connector


# =========================
# MySQL Database Connection
# =========================

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="library_db"
    )


# =========================
# Add Book Function
# =========================

def add_book():

    add_window = tk.Toplevel()
    add_window.title("Add Book")
    add_window.geometry("450x400")
    add_window.resizable(False, False)

    tk.Label(
        add_window,
        text="Add New Book",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        add_window,
        text="Book ID",
        font=("Arial", 12)
    ).pack()

    book_id_entry = tk.Entry(
        add_window,
        font=("Arial", 12)
    )
    book_id_entry.pack(pady=5)

    tk.Label(
        add_window,
        text="Book Title",
        font=("Arial", 12)
    ).pack()

    title_entry = tk.Entry(
        add_window,
        font=("Arial", 12)
    )
    title_entry.pack(pady=5)

    tk.Label(
        add_window,
        text="Publisher ID",
        font=("Arial", 12)
    ).pack()

    publisher_id_entry = tk.Entry(
        add_window,
        font=("Arial", 12)
    )
    publisher_id_entry.pack(pady=5)

    def save_book():

        book_id = book_id_entry.get()
        title = title_entry.get()
        publisher_id = publisher_id_entry.get()

        if book_id == "" or title == "" or publisher_id == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            query = """
            INSERT INTO books
            (book_id, title, publisher_id)
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (book_id, title, publisher_id)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Book added successfully!"
            )

            book_id_entry.delete(0, tk.END)
            title_entry.delete(0, tk.END)
            publisher_id_entry.delete(0, tk.END)

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                str(err)
            )

    tk.Button(
        add_window,
        text="Add Book",
        font=("Arial", 12, "bold"),
        width=15,
        command=save_book
    ).pack(pady=20)


# =========================
# View Books Function
# =========================

def view_books():

    view_window = tk.Toplevel()
    view_window.title("View Books")
    view_window.geometry("650x400")
    view_window.resizable(False, False)

    tk.Label(
        view_window,
        text="Library Books",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    try:

        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT books.book_id,
               books.title,
               publisher.name
        FROM books
        LEFT JOIN publisher
        ON books.publisher_id = publisher.publisher_id
        """

        cursor.execute(query)

        records = cursor.fetchall()

        cursor.close()
        conn.close()

        tk.Label(
            view_window,
            text="Book ID        Title                    Publisher",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        if records:

            for book_id, title, publisher in records:

                if publisher is None:
                    publisher = "Not Available"

                tk.Label(
                    view_window,
                    text=f"{book_id:<15}{title:<25}{publisher}",
                    font=("Arial", 11)
                ).pack(pady=3)

        else:

            tk.Label(
                view_window,
                text="No books found.",
                font=("Arial", 12)
            ).pack(pady=20)

    except mysql.connector.Error as err:

        messagebox.showerror(
            "Database Error",
            str(err)
        )


# =========================
# Search Book Function
# =========================

def search_book():

    search_window = tk.Toplevel()
    search_window.title("Search Book")
    search_window.geometry("500x400")
    search_window.resizable(False, False)

    tk.Label(
        search_window,
        text="Search Book",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    tk.Label(
        search_window,
        text="Enter Book ID",
        font=("Arial", 12)
    ).pack()

    book_id_entry = tk.Entry(
        search_window,
        font=("Arial", 12)
    )
    book_id_entry.pack(pady=8)

    def find_book():

        book_id = book_id_entry.get()

        if book_id == "":
            messagebox.showwarning(
                "Warning",
                "Please enter Book ID"
            )
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            query = """
            SELECT books.book_id,
                   books.title,
                   publisher.name
            FROM books
            LEFT JOIN publisher
            ON books.publisher_id = publisher.publisher_id
            WHERE books.book_id = %s
            """

            cursor.execute(
                query,
                (book_id,)
            )

            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:

                book_id, title, publisher = result

                if publisher is None:
                    publisher = "Not Available"

                messagebox.showinfo(
                    "Book Found",
                    f"Book ID: {book_id}\n"
                    f"Title: {title}\n"
                    f"Publisher: {publisher}"
                )

            else:

                messagebox.showerror(
                    "Not Found",
                    "Book not found."
                )

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                str(err)
            )

    tk.Button(
        search_window,
        text="Search",
        font=("Arial", 12, "bold"),
        width=15,
        command=find_book
    ).pack(pady=20)


# =========================
# Add Member Function
# =========================

def add_member():

    member_window = tk.Toplevel()
    member_window.title("Add Member")
    member_window.geometry("450x500")
    member_window.resizable(False, False)

    tk.Label(
        member_window,
        text="Add New Member",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # Reader ID
    tk.Label(
        member_window,
        text="Reader ID",
        font=("Arial", 12)
    ).pack()

    reader_id_entry = tk.Entry(
        member_window,
        font=("Arial", 12)
    )
    reader_id_entry.pack(pady=5)

    # Reader Name
    tk.Label(
        member_window,
        text="Reader Name",
        font=("Arial", 12)
    ).pack()

    reader_name_entry = tk.Entry(
        member_window,
        font=("Arial", 12)
    )
    reader_name_entry.pack(pady=5)

    # Phone
    tk.Label(
        member_window,
        text="Phone",
        font=("Arial", 12)
    ).pack()

    phone_entry = tk.Entry(
        member_window,
        font=("Arial", 12)
    )
    phone_entry.pack(pady=5)

    # User ID
    tk.Label(
        member_window,
        text="User ID",
        font=("Arial", 12)
    ).pack()

    user_id_entry = tk.Entry(
        member_window,
        font=("Arial", 12)
    )
    user_id_entry.pack(pady=5)

    # Email
    tk.Label(
        member_window,
        text="Email",
        font=("Arial", 12)
    ).pack()

    email_entry = tk.Entry(
        member_window,
        font=("Arial", 12)
    )
    email_entry.pack(pady=5)

    def save_member():

        reader_id = reader_id_entry.get()
        reader_name = reader_name_entry.get()
        phone = phone_entry.get()
        user_id = user_id_entry.get()
        email = email_entry.get()

        if (
            reader_id == ""
            or reader_name == ""
            or phone == ""
            or user_id == ""
            or email == ""
        ):
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            query = """
            INSERT INTO reader
            (reader_id, reader_name, phone, user_id, email)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    reader_id,
                    reader_name,
                    phone,
                    user_id,
                    email
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Member added successfully!"
            )

            reader_id_entry.delete(0, tk.END)
            reader_name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            user_id_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                str(err)
            )

    tk.Button(
        member_window,
        text="Add Member",
        font=("Arial", 12, "bold"),
        width=15,
        command=save_member
    ).pack(pady=20)


# =========================
# Issue Book Function
# =========================

def issue_book():

    issue_window = tk.Toplevel()
    issue_window.title("Issue Book")
    issue_window.geometry("450x450")
    issue_window.resizable(False, False)

    tk.Label(
        issue_window,
        text="Issue Book",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # Issue ID
    tk.Label(
        issue_window,
        text="Issue ID",
        font=("Arial", 12)
    ).pack()

    issue_id_entry = tk.Entry(
        issue_window,
        font=("Arial", 12)
    )
    issue_id_entry.pack(pady=5)

    # Book ID
    tk.Label(
        issue_window,
        text="Book ID",
        font=("Arial", 12)
    ).pack()

    book_id_entry = tk.Entry(
        issue_window,
        font=("Arial", 12)
    )
    book_id_entry.pack(pady=5)

    # Reader ID
    tk.Label(
        issue_window,
        text="Reader ID",
        font=("Arial", 12)
    ).pack()

    reader_id_entry = tk.Entry(
        issue_window,
        font=("Arial", 12)
    )
    reader_id_entry.pack(pady=5)

    # Issue Date
    tk.Label(
        issue_window,
        text="Issue Date (YYYY-MM-DD)",
        font=("Arial", 12)
    ).pack()

    issue_date_entry = tk.Entry(
        issue_window,
        font=("Arial", 12)
    )
    issue_date_entry.pack(pady=5)

    def save_issue():

        issue_id = issue_id_entry.get()
        book_id = book_id_entry.get()
        reader_id = reader_id_entry.get()
        issue_date = issue_date_entry.get()

        if (
            issue_id == ""
            or book_id == ""
            or reader_id == ""
            or issue_date == ""
        ):
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            # Check whether book exists
            cursor.execute(
                "SELECT book_id FROM books WHERE book_id = %s",
                (book_id,)
            )

            book = cursor.fetchone()

            if book is None:

                messagebox.showerror(
                    "Error",
                    "Book ID does not exist."
                )

                cursor.close()
                conn.close()
                return

            # Check whether reader exists
            cursor.execute(
                "SELECT reader_id FROM reader WHERE reader_id = %s",
                (reader_id,)
            )

            reader = cursor.fetchone()

            if reader is None:

                messagebox.showerror(
                    "Error",
                    "Reader ID does not exist."
                )

                cursor.close()
                conn.close()
                return

            # Insert issue record
            query = """
            INSERT INTO issue
            (issue_id, book_id, reader_id, issue_date)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    issue_id,
                    book_id,
                    reader_id,
                    issue_date
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Book issued successfully!"
            )

            issue_id_entry.delete(0, tk.END)
            book_id_entry.delete(0, tk.END)
            reader_id_entry.delete(0, tk.END)
            issue_date_entry.delete(0, tk.END)

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                str(err)
            )

    tk.Button(
        issue_window,
        text="Issue Book",
        font=("Arial", 12, "bold"),
        width=15,
        command=save_issue
    ).pack(pady=20)


# =========================
# Return Book Function
# =========================

def return_book():

    return_window = tk.Toplevel()
    return_window.title("Return Book")
    return_window.geometry("450x300")
    return_window.resizable(False, False)

    tk.Label(
        return_window,
        text="Return Book",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # Issue ID
    tk.Label(
        return_window,
        text="Issue ID",
        font=("Arial", 12)
    ).pack()

    issue_id_entry = tk.Entry(
        return_window,
        font=("Arial", 12)
    )
    issue_id_entry.pack(pady=5)

    # Return Date
    tk.Label(
        return_window,
        text="Return Date (YYYY-MM-DD)",
        font=("Arial", 12)
    ).pack()

    return_date_entry = tk.Entry(
        return_window,
        font=("Arial", 12)
    )
    return_date_entry.pack(pady=5)

    def save_return():

        issue_id = issue_id_entry.get()
        return_date = return_date_entry.get()

        if issue_id == "" or return_date == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            # Check issue ID
            cursor.execute(
                "SELECT issue_id, return_date FROM issue WHERE issue_id = %s",
                (issue_id,)
            )

            result = cursor.fetchone()

            if result is None:

                messagebox.showerror(
                    "Error",
                    "Issue ID not found."
                )

                cursor.close()
                conn.close()
                return

            # Check if already returned
            if result[1] is not None:

                messagebox.showwarning(
                    "Warning",
                    "This book has already been returned."
                )

                cursor.close()
                conn.close()
                return

            # Update return date
            query = """
            UPDATE issue
            SET return_date = %s
            WHERE issue_id = %s
            """

            cursor.execute(
                query,
                (
                    return_date,
                    issue_id
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Book returned successfully!"
            )

            issue_id_entry.delete(0, tk.END)
            return_date_entry.delete(0, tk.END)

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                str(err)
            )

    tk.Button(
        return_window,
        text="Return Book",
        font=("Arial", 12, "bold"),
        width=15,
        command=save_return
    ).pack(pady=20)


# =========================
# Dashboard Function
# =========================

def open_dashboard():

    login_window.destroy()

    dashboard = tk.Tk()

    dashboard.title(
        "Library Management System"
    )

    dashboard.geometry("700x600")

    dashboard.resizable(False, False)

    # Title
    tk.Label(
        dashboard,
        text="Library Management System",
        font=("Arial", 22, "bold")
    ).pack(pady=30)

    # Welcome Message
    tk.Label(
        dashboard,
        text="Welcome to the Library Dashboard",
        font=("Arial", 14)
    ).pack(pady=10)

    # Add Book
    tk.Button(
        dashboard,
        text="Add Book",
        font=("Arial", 12),
        width=25,
        command=add_book
    ).pack(pady=5)

    # View Books
    tk.Button(
        dashboard,
        text="View Books",
        font=("Arial", 12),
        width=25,
        command=view_books
    ).pack(pady=5)

    # Search Book
    tk.Button(
        dashboard,
        text="Search Book",
        font=("Arial", 12),
        width=25,
        command=search_book
    ).pack(pady=5)

    # Add Member
    tk.Button(
        dashboard,
        text="Add Member",
        font=("Arial", 12),
        width=25,
        command=add_member
    ).pack(pady=5)

    # Issue Book
    tk.Button(
        dashboard,
        text="Issue Book",
        font=("Arial", 12),
        width=25,
        command=issue_book
    ).pack(pady=5)

    # Return Book
    tk.Button(
        dashboard,
        text="Return Book",
        font=("Arial", 12),
        width=25,
        command=return_book
    ).pack(pady=5)

    # Logout
    tk.Button(
        dashboard,
        text="Logout",
        font=("Arial", 12, "bold"),
        width=25,
        command=dashboard.destroy
    ).pack(pady=20)

    dashboard.mainloop()


# =========================
# Login Function
# =========================

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password"
        )
        return

    try:

        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT *
        FROM users
        WHERE username = %s
        AND password = %s
        """

        cursor.execute(
            query,
            (username, password)
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:

            messagebox.showinfo(
                "Success",
                "Login Successful!"
            )

            open_dashboard()

        else:

            messagebox.showerror(
                "Error",
                "Invalid username or password"
            )

    except mysql.connector.Error as err:

        messagebox.showerror(
            "Database Error",
            str(err)
        )


# =========================
# Login Window
# =========================

login_window = tk.Tk()

login_window.title(
    "Library Management System - Login"
)

login_window.geometry("450x350")

login_window.resizable(False, False)


# Main Title
tk.Label(
    login_window,
    text="Library Management System",
    font=("Arial", 18, "bold")
).pack(pady=20)


# Username Label
tk.Label(
    login_window,
    text="Username",
    font=("Arial", 12)
).pack()


# Username Entry
username_entry = tk.Entry(
    login_window,
    font=("Arial", 12)
)

username_entry.pack(pady=5)


# Password Label
tk.Label(
    login_window,
    text="Password",
    font=("Arial", 12)
).pack()


# Password Entry
password_entry = tk.Entry(
    login_window,
    font=("Arial", 12),
    show="*"
)

password_entry.pack(pady=5)


# Login Button
tk.Button(
    login_window,
    text="Login",
    font=("Arial", 12, "bold"),
    width=15,
    command=login
).pack(pady=20)


# =========================
# Start Application
# =========================

login_window.mainloop()