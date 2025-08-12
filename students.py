import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

students = []
student_id_counter = 1

# Add student
def add_student():
    global student_id_counter
    name = entry_name.get()
    age = entry_age.get()
    grade = entry_grade.get()

    if not name or not age or not grade:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number!")
        return

    students.append({"ID": student_id_counter, "Name": name, "Age": age, "Grade": grade})
    student_id_counter += 1
    messagebox.showinfo("Success", f"Student '{name}' added successfully!")
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_grade.delete(0, tk.END)

# View all students
def view_students(filtered=None):
    win = tk.Toplevel(root)
    win.title("View Students")
    win.geometry("500x300")

    table = ttk.Treeview(win, columns=("ID", "Name", "Age", "Grade"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Name", text="Name")
    table.heading("Age", text="Age")
    table.heading("Grade", text="Grade")
    table.pack(fill=tk.BOTH, expand=True)

    data_to_show = filtered if filtered is not None else students
    for student in data_to_show:
        table.insert("", tk.END, values=(student["ID"], student["Name"], student["Age"], student["Grade"]))

# Search students
def search_student():
    term = simpledialog.askstring("Search", "Enter Student Name or ID:")
    if not term:
        return

    try:
        term = int(term)
        results = [s for s in students if s["ID"] == term]
    except ValueError:
        results = [s for s in students if term.lower() in s["Name"].lower()]

    if results:
        view_students(results)
    else:
        messagebox.showinfo("Search", "No matching students found.")

# Update student
def update_student():
    try:
        sid = int(simpledialog.askstring("Update Student", "Enter Student ID to update:"))
    except (ValueError, TypeError):
        return

    for student in students:
        if student["ID"] == sid:
            new_name = simpledialog.askstring("Update", f"Enter new name ({student['Name']}):") or student["Name"]
            try:
                new_age = simpledialog.askstring("Update", f"Enter new age ({student['Age']}):")
                new_age = int(new_age) if new_age else student["Age"]
            except ValueError:
                messagebox.showerror("Error", "Age must be a number!")
                return
            new_grade = simpledialog.askstring("Update", f"Enter new grade ({student['Grade']}):") or student["Grade"]

            student["Name"] = new_name
            student["Age"] = new_age
            student["Grade"] = new_grade
            messagebox.showinfo("Success", "Student updated successfully!")
            return

    messagebox.showerror("Error", "Student ID not found.")

# Delete student
def delete_student():
    try:
        sid = int(simpledialog.askstring("Delete Student", "Enter Student ID to delete:"))
    except (ValueError, TypeError):
        return

    for student in students:
        if student["ID"] == sid:
            students.remove(student)
            messagebox.showinfo("Success", "Student deleted successfully!")
            return

    messagebox.showerror("Error", "Student ID not found.")

# Clear all students (reset IDs)
def clear_students():
    global student_id_counter
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all students?"):
        students.clear()
        student_id_counter = 1
        messagebox.showinfo("Success", "All students cleared and IDs reset.")

# GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("400x350")

tk.Label(root, text="Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Age:").pack()
entry_age = tk.Entry(root)
entry_age.pack()

tk.Label(root, text="Grade:").pack()
entry_grade = tk.Entry(root)
entry_grade.pack()

tk.Button(root, text="Add Student", command=add_student).pack(pady=5)
tk.Button(root, text="View Students", command=view_students).pack(pady=5)
tk.Button(root, text="Search Student", command=search_student).pack(pady=5)
tk.Button(root, text="Update Student", command=update_student).pack(pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(pady=5)
tk.Button(root, text="Clear All Students", command=clear_students).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

root.mainloop()
