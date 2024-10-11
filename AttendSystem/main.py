from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import time
import bcrypt
import mysql.connector
from Database.database import Database

# ======================= LOGIN=WINDOW ================================#    
class Login_Window:
    def __init__(self, window, db):
        self.db = db
        self.window = window
        self.window.title("Login Window")
        self.window.configure(bg="white")
        self.window.geometry("1000x600+300+90")
        self.create_widgets()

    def create_widgets(self):
        # UM Label
        umlabel = Label(self.window, text="UM", font=("Arial", 120,), fg="maroon", bg="white")
        umlabel.place(x=170, y=170, width=220, height=180)

        # Slogan Label
        oa = Label(self.window, text="Bahalag ge kapoy basta GA-padayon japon.", font=("Arial", 11), bg="white")
        oa.place(x=150, y=350, width=280, height=20)

        # Login Label
        login_label = Label(self.window, text="Log in", font=("Arial", 20), bg="white", fg="maroon")
        login_label.place(x=740, y=70, width=180, height=160)

        # Username Label and Entry
        reg_username = Label(self.window, text="Username:", font=("Arial", 11), bg="white", fg="black")
        reg_username.place(x=575, y=240, width=120, height=30)

        username_placeholder = "Username"
        self.regenter_username = Entry(self.window, font=("Arial", 11), fg="grey", bg="white")
        self.regenter_username.bind("<FocusIn>", lambda event: self.when_enter(event, self.regenter_username, username_placeholder))
        self.regenter_username.bind("<FocusOut>", lambda event: self.when_not_enter(event, self.regenter_username, username_placeholder))
        self.regenter_username.insert(0, username_placeholder)
        self.regenter_username.place(x=700, y=240, width=250, height=30)

        # Password Label and Entry
        reg_password = Label(self.window, text="Password:", font=("Arial", 11), bg="white", fg="black")
        reg_password.place(x=575, y=300, width=120, height=30)

        password_placeholder = "Password"
        self.regenter_password = Entry(self.window, font=("Arial", 11), fg='grey', bg="white", show="*")
        self.regenter_password.bind("<FocusIn>", lambda event: self.when_enter_password(event, self.regenter_password, password_placeholder))
        self.regenter_password.bind("<FocusOut>", lambda event: self.when_not_enter_password(event, self.regenter_password, password_placeholder))
        self.regenter_password.insert(0, password_placeholder)
        self.regenter_password.place(x=700, y=300, width=250, height=30)

        # Login Button
        login_button = Button(self.window, text="Log in", font=("Arial", 12), width=15, command=self.login, bg="maroon", fg="white")
        login_button.place(x=750, y=360)

        # Create Account Section
        create_acc = Label(self.window, text="Don't have an account?", font=("Arial", 13), bg="white")
        create_acc.place(x=730, y=420, width=190, height=60)

        createacc_button = Button(self.window, text="Create Account", font=("Arial", 13), width=25, command=self.createacc_window, bg="maroon", fg="white")
        createacc_button.place(x=710, y=480)

    def when_enter(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")

    def when_not_enter(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def when_enter_password(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black", show="*")

    def when_not_enter_password(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey", show="*")

    def createacc_window(self):
        self.window.withdraw()
        createaccWindow = Toplevel(self.window)
        CreateAccount_Window(createaccWindow, self, self.db)

    def open_table(self):
        self.window.withdraw()
        open_attendance = Toplevel(self.window)
        Table_Window(open_attendance, self, self.db)

    def check_credentials(self, username, password):
        try:
            query = "SELECT password FROM user WHERE username = %s"
            result = self.db.fetch_one(query, (username,))
            if result:
                stored_password = result[0].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    return True
            return False
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return False

    def login(self):
        username = self.regenter_username.get()
        password = self.regenter_password.get()

        # Remove placeholders if present
        if username == "Username":
            username = ""
        if password == "Password":
            password = ""

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        if self.check_credentials(username, password):
            messagebox.showinfo("Success", "Logged in successfully!")
            self.open_table()
        else:
            messagebox.showerror("Error", "Invalid username or password")

# ======================= CREATE ACCOUNT WINDOW ================================ #
class CreateAccount_Window:
    def __init__(self, window, login_window, db):
        self.login_window = login_window
        self.db = db
        self.window = window
        self.window.title("Create Account")
        self.window.config(bg="white")
        self.window.geometry("420x300+580+230")

        self.create_widgets()

    def create_widgets(self):
        # Header Label
        label1 = Label(self.window, text="Create account to log in", font=("Arial", 15), bg="white", fg="maroon")
        label1.place(x=110, y=10, width=220, height=50)

        # Email Label and Entry
        emaillabel = Label(self.window, text="Email:", font=("Arial", 11), bg="white")
        emaillabel.place(x=105, y=80, width=110, height=25)

        self.emailentry = Entry(self.window, font=("Arial", 11), bg="white")
        self.emailentry.place(x=200, y=80, width=170, height=25)

        # Username Label and Entry
        usernamelabel = Label(self.window, text="Username:", font=("Arial", 11), bg="white")
        usernamelabel.place(x=90, y=120, width=110, height=25)

        self.unentry = Entry(self.window, font=("Arial", 11), bg="white")
        self.unentry.place(x=200, y=120, width=170, height=25)

        # Password Label and Entry
        passlabel = Label(self.window, text="Password:", font=("Arial", 11), bg="white")
        passlabel.place(x=90, y=160, width=110, height=25)

        self.passentry = Entry(self.window, font=("Arial", 11), bg="white", show="*")
        self.passentry.place(x=200, y=160, width=170, height=25)

        # Re-Enter Password Label and Entry
        repasslabel = Label(self.window, text="Re-Enter password:", font=("Arial", 11), bg="white")
        repasslabel.place(x=40, y=200, width=150, height=25)

        self.repassentry = Entry(self.window, font=("Arial", 11), bg="white", show="*")
        self.repassentry.place(x=200, y=200, width=170, height=25)

        # Register Button
        register_account = Button(self.window, text="Create Account", font=("Arial", 11), width=15, bg="maroon", fg="white", command=self.register_account)
        register_account.place(x=255, y=250)

        # Back Button
        backlogin = Button(self.window, text="Back", font=("Arial", 11), width=10, command=self.backto_loginframe, bg="maroon", fg="white")
        backlogin.place(x=20, y=250)

    def backto_loginframe(self):
        self.window.destroy()
        self.login_window.window.deiconify()

    def register_account(self):
        email = self.emailentry.get().strip()
        username = self.unentry.get().strip()
        password = self.passentry.get()
        re_password = self.repassentry.get()

        if not email or not username or not password or not re_password:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        if password != re_password:
            messagebox.showerror("Input Error", "Passwords do not match.")
            return

        try:
            # Check if username already exists
            existing_query = "SELECT * FROM user WHERE username = %s"
            existing_user = self.db.fetch_one(existing_query, (username,))

            if existing_user:
                messagebox.showerror("Error", "Username already exists.")
                return

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert the new user into the database
            insert_query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            self.db.execute_query(insert_query, (username, hashed_password.decode('utf-8'), email))

            messagebox.showinfo("Success", "Account created successfully")
            self.backto_loginframe()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to create account: {e}")
        except Exception as ex:
            messagebox.showerror("Error", f"An unexpected error occurred: {ex}")

# ======================= TABLE WINDOW ================================ #
class Table_Window:
    def __init__(self, window, login_window, db):
        self.window = window
        self.login_window = login_window
        self.db = db
        self.window.title("Attendance")
        self.window.geometry("1200x700+180+50")

        # Define shades of maroon
        dark_maroon = '#800000'
        light_maroon = '#D8A4A4'
        medium_maroon = '#A52A2A'
        button_maroon = '#B03060'
        entry_bg = '#FAE3E3'
        text_color = '#FFF'

        # Define Treeview colors (light maroon)
        tree_bg = '#F5D4D4'  
        tree_fg = '#000'     
        tree_sel_bg = '#D89B9B'  
        tree_sel_fg = '#FFF'    

        # Panel background color
        panel1 = Frame(self.window, bd=5, relief="ridge", bg=medium_maroon)
        panel1.place(x=5, y=5, width=1190, height=240)

        # Student Info Label
        student_info = Label(panel1, text="Input Student's Info to add in the attendance:", font=("Arial", 17), bg=medium_maroon, fg=text_color)
        student_info.place(x=15, y=15, width=450, height=35)

        # Date Label
        Date = Label(panel1, text="Date:", font=("Arial", 14), bg=medium_maroon, fg=text_color)
        Date.place(x=800, y=15, width=100, height=30)

        self.date = Label(panel1, text="OK", font=("Arial", 12), bg=medium_maroon, fg=text_color)
        self.date.place(x=870, y=15, width=190, height=30)

        # Time Label
        Time = Label(panel1, text="Time:", font=("Arial", 14), bg=medium_maroon, fg=text_color)
        Time.place(x=800, y=50, width=100, height=30)

        self.time = Label(panel1, text="OK", font=("Arial", 12), bg=medium_maroon, fg=text_color)
        self.time.place(x=900, y=50, width=100, height=30)

        # Start running time
        self.running_time()

        # ID Label and Entry
        idlabel = Label(panel1, text="ID:", font=("Arial", 12), bg=medium_maroon, fg=text_color)
        idlabel.place(x=10, y=70, width=110, height=25)

        self.identer = Entry(panel1, font=("Arial", 14), bg=entry_bg)
        self.identer.place(x=130, y=70, width=220, height=25)

        # Last Name Label and Entry
        lastname = Label(panel1, text="Last Name:", font=("Arial", 12), bg=medium_maroon, fg=text_color)
        lastname.place(x=10, y=130, width=110, height=25)

        self.lastname_entry = Entry(panel1, font=("Arial", 12), bg=entry_bg)
        self.lastname_entry.place(x=130, y=130, width=220, height=25)

        # First Name Label and Entry
        firstname = Label(panel1, text="First Name:", font=("Arial", 12), bg=medium_maroon, fg=text_color)
        firstname.place(x=400, y=130, width=120, height=25)

        self.firstname_entry = Entry(panel1, font=("Arial", 12), bg=entry_bg)
        self.firstname_entry.place(x=520, y=130, width=220, height=25)

        # Middle Name Label and Entry
        middlename = Label(panel1, text="Middle Name:", font=("Arial", 12), bg=medium_maroon, fg=text_color)
        middlename.place(x=800, y=130, width=130, height=25)

        self.middlename_entry = Entry(panel1, font=("Arial", 12), bg=entry_bg)
        self.middlename_entry.place(x=930, y=130, width=220, height=25)

        # Add Button
        addbutton = Button(panel1, text="Add", font=("Arial", 12), bg=button_maroon, fg=text_color, command=self.add_student)
        addbutton.place(x=960, y=190, width=90, height=25)

        # Edit Button
        editbutton = Button(panel1, text="Edit", font=("Arial", 12), bg=button_maroon, fg=text_color, command=self.edit_student)
        editbutton.place(x=1070, y=190, width=90, height=25)

        # Save Button
        savebutton = Button(self.window, text="Save", font=("Arial", 12), bg=dark_maroon, fg=text_color, command=self.save_data)
        savebutton.place(x=980, y=660, width=90, height=25)

        # Drop Button
        dropbutton = Button(self.window, text="Drop", font=("Arial", 12), bg=dark_maroon, fg=text_color, command=self.drop_student)
        dropbutton.place(x=1090, y=660, width=90, height=25)

        # Back Button
        backbutton = Button(self.window, text="Back", font=("Arial", 12), command=self.back_to_login, bg=dark_maroon, fg=text_color)
        backbutton.place(x=10, y=660, width=90, height=25)

        # Style the Treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview",
                        background=tree_bg,
                        foreground=tree_fg,
                        fieldbackground=tree_bg,
                        rowheight=25
                        ) 

        style.map("mystyle.Treeview",
                  background=[("selected", tree_sel_bg)],
                  foreground=[("selected", tree_sel_fg)]
        )

        # Table panel background
        self.tablepanel = Frame(self.window, bd=5, relief="ridge", bg=light_maroon)
        self.tablepanel.place(x=5, y=250, width=1190, height=390)

        # Define columns
        self.columns = ("ID", "Student's Name", "Status")
        self.table = ttk.Treeview(self.tablepanel, columns=self.columns, show='headings', style="mystyle.Treeview")

        # Define headings
        self.table.heading("ID", text="ID")
        self.table.heading("Student's Name", text="Student's Name")
        self.table.heading("Status", text="Status")

        # Define column properties
        self.table.column("ID", width=50, anchor="center")
        self.table.column("Student's Name", width=180, anchor="center")
        self.table.column("Status", width=100, anchor="center")

        self.table.pack(ipadx=10, ipady=60, fill=BOTH)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.tablepanel, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Bind click event
        self.table.bind("<Button-1>", self.on_click_item)

        # Load existing attendance records
        self.load_attendance()

    #Load attendance records from the database into the Treeview
    def load_attendance(self):
        try:
            query = "SELECT student_id, name, status FROM attendance"
            records = self.db.fetch_data(query)
            for record in records:
                self.table.insert("", END, values=record)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load attendance records: {e}")

    #Add a new student to the attendance
    def add_student(self):
        try:
            student_id = int(self.identer.get())
        except ValueError:
            messagebox.showerror("Error Input", "ID must be a numerical value.")
            return

        last_name = self.lastname_entry.get().strip()
        first_name = self.firstname_entry.get().strip()
        middle_name = self.middlename_entry.get().strip()

        if not last_name or not first_name:
            messagebox.showerror("Error Input", "First and Last names are required.")
            return

        # Check if student_id already exists in the database
        try:
            check_query = "SELECT * FROM attendance WHERE student_id = %s"
            existing_student = self.db.fetch_one(check_query, (student_id,))
            if existing_student:
                messagebox.showerror("Input Error", "This ID is already taken.")
                return
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to check student ID: {e}")
            return

        full_name = f"{last_name}, {first_name} {middle_name}".strip()
        new_row = (student_id, full_name, "Present")

        # Insert into the Treeview
        self.table.insert("", "end", values=new_row)

        # Add to the database
        try:
            insert_query = "INSERT INTO attendance (student_id, name, status) VALUES (%s, %s, %s)"
            self.db.execute_query(insert_query, (student_id, full_name, "Present"))
            messagebox.showinfo("Success", "Student added successfully.")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add student: {e}")

    #Edit selected student's information
    def edit_student(self):
        selected_item = self.table.selection()
        if selected_item:
            student_id = self.table.item(selected_item[0], "values")[0]
            name = self.table.item(selected_item[0], "values")[1]
            status = self.table.item(selected_item[0], "values")[2]

            # Split the name into last, first, and middle names
            try:
                last_name, rest = name.split(",", 1)
                first_name, middle_name = rest.strip().split(" ", 1)
            except ValueError:
                last_name = name.split(",")[0]
                first_name = ""
                middle_name = ""

            # Populate the entry fields with existing data
            self.identer.delete(0, END)
            self.identer.insert(0, student_id)
            self.lastname_entry.delete(0, END)
            self.lastname_entry.insert(0, last_name)
            self.firstname_entry.delete(0, END)
            self.firstname_entry.insert(0, first_name)
            self.middlename_entry.delete(0, END)
            self.middlename_entry.insert(0, middle_name)

            # Change the Add button to Update
            def update_student():
                updated_id = self.identer.get()
                updated_last_name = self.lastname_entry.get().strip()
                updated_first_name = self.firstname_entry.get().strip()
                updated_middle_name = self.middlename_entry.get().strip()

                if not updated_last_name or not updated_first_name:
                    messagebox.showerror("Error Input", "First and Last names are required.")
                    return

                updated_full_name = f"{updated_last_name}, {updated_first_name} {updated_middle_name}".strip()

                # Update the Treeview
                self.table.item(selected_item[0], values=(updated_id, updated_full_name, status))

                # Update the database
                try:
                    update_query = "UPDATE attendance SET student_id = %s, name = %s, status = %s WHERE student_id = %s"
                    self.db.execute_query(update_query, (updated_id, updated_full_name, status, student_id))
                    messagebox.showinfo("Success", "Student information updated successfully.")
                    self.clear_entries()
                    addbutton.config(text="Add", command=self.add_student)
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to update student: {e}")

            # Change the Add button to Update
            addbutton = self.window.children.get('!frame').children.get('!button')
            addbutton.config(text="Update", command=update_student)
        else:
            messagebox.showerror("Selection Error", "Please select a student to edit.")
       
    #Change the status of a student
    def change_status(self, student_id, current_status):
        statuses = ["Present", "Absent", "Excused"]
        if current_status in statuses:
            next_status = statuses[(statuses.index(current_status) + 1) % len(statuses)]
        else:
            next_status = "Present"

        # Update the Treeview
        for row in self.table.get_children():
            if self.table.item(row, "values")[0] == student_id:
                self.table.item(row, values=(student_id, self.table.item(row, "values")[1], next_status))
                break

        # Update the database
        try:
            update_query = "UPDATE attendance SET status = %s WHERE student_id = %s"
            self.db.execute_query(update_query, (next_status, student_id))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update status: {e}")

    #Handle click on Treeview item to change status
    def on_click_item(self, event):
        item = self.table.identify_row(event.y)
        if item:
            student_id = self.table.item(item, "values")[0]
            current_status = self.table.item(item, "values")[2]
            self.change_status(student_id, current_status)
       
    #Optional ni siya kung i-implement ang function then save
    def save_data(self):
        # Since changes are saved in real-time, this might not be necessary.
        messagebox.showinfo("Save", "All changes have been saved to the database.")

    #Delete a selected student from attendance
    def drop_student(self):
        selected_item = self.table.selection()
        if selected_item:
            student_id = self.table.item(selected_item[0], "values")[0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {student_id}?")
            if confirm:
                try:
                    delete_query = "DELETE FROM attendance WHERE student_id = %s"
                    self.db.execute_query(delete_query, (student_id,))
                    self.table.delete(selected_item[0])
                    messagebox.showinfo("Delete Successful", "Student data deleted successfully.")
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to delete student: {e}")
        else:
            messagebox.showerror("Selection Error", "Please select a student to delete.")

    #Update the date and time labels every second
    def running_time(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        self.date.config(text=current_date)
        self.time.config(text=current_time)
        self.window.after(1000, self.running_time)

    #Clear all entry fields
    def clear_entries(self):
        self.identer.delete(0, END)
        self.lastname_entry.delete(0, END)
        self.firstname_entry.delete(0, END)
        self.middlename_entry.delete(0, END)

    #Return to the login window."""
    def back_to_login(self):
        self.window.destroy()
        self.login_window.window.deiconify()

# ======================= MAIN APPLICATION ================================ #
def main():
    # Initialize Database Connection
    db = Database(host="localhost", database="attendsystem", user="root", password="")
    try:
        db.connect()
    except Exception as e:
        messagebox.showerror("Database Connection Error", f"Cannot connect to the database: {e}")
        return

    # Create the main window for login
    root = Tk()
    app = Login_Window(root, db)
    root.mainloop()

    # Close the database connection when the application closes
    db.close_connection()

if __name__ == "__main__":
    main()