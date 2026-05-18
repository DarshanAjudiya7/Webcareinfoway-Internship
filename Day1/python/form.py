import tkinter as tk
from tkinter import messagebox, ttk
import re

def submit_form():
    name_val = namei.get()
    age_val = agei.get()
    email_val = emaili.get()
    
    day = day_var.get()
    month = month_var.get()
    year = year_var.get()
    dob_val = f"{day} {month} {year}"
    
    gender_val = gender_var.get()

    languages = []
    if python_var.get(): languages.append("Python")
    if cpp_var.get(): languages.append("C++")
    if java_var.get(): languages.append("Java")
    
    lang_str = ", ".join(languages) if languages else "None"

    if not name_val or not age_val or not email_val or not day or not month or not year or gender_val == "None":
        messagebox.showwarning("Form Warning", "Please fill in all fields")
        return

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email_val):
        messagebox.showerror("Error", "Invalid email format")
        return
    
    try:
        age_int = int(age_val)
        if age_int < 1 or age_int > 100:
            messagebox.showerror("Error", "Invalid age (must be 1-100)")
            return
    except ValueError:
        messagebox.showerror("Error", "Age must be a number")
        return

    result = f"--- Student Submitted Details ---\nName: {name_val}\nAge: {age_val}\nEmail: {email_val}\nDOB: {dob_val}\nGender: {gender_val}\nLanguages: {lang_str}"
    result_label.config(text=result)

root = tk.Tk()
root.title("Student Information Form")
root.geometry("500x750")

tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
namei = tk.Entry(root)
namei.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Age:").grid(row=1, column=0, padx=10, pady=10)
agei = tk.Entry(root)
agei.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=10)
emaili = tk.Entry(root)
emaili.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Birth Date:").grid(row=3, column=0, padx=10, pady=10)
dob_frame = tk.Frame(root)
dob_frame.grid(row=3, column=1)

day_var = tk.StringVar()
month_var = tk.StringVar()
year_var = tk.StringVar()

days = [str(i).zfill(2) for i in range(1, 32)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [str(i) for i in range(2024, 1949, -1)]

day_cb = ttk.Combobox(dob_frame, textvariable=day_var, values=days, width=3)
day_cb.pack(side="left", padx=2)
month_cb = ttk.Combobox(dob_frame, textvariable=month_var, values=months, width=5)
month_cb.pack(side="left", padx=2)
year_cb = ttk.Combobox(dob_frame, textvariable=year_var, values=years, width=5)
year_cb.pack(side="left", padx=2)

tk.Label(root, text="Gender:").grid(row=4, column=0, padx=10, pady=10)
gender_var = tk.StringVar(value="None")
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").grid(row=4, column=1)
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").grid(row=5, column=1)
tk.Radiobutton(root, text="Other", variable=gender_var, value="Other").grid(row=6, column=1)

tk.Label(root, text="Languages:").grid(row=7, column=0, padx=10, pady=10)
python_var = tk.BooleanVar()
cpp_var = tk.BooleanVar()
java_var = tk.BooleanVar()

tk.Checkbutton(root, text="Python", variable=python_var).grid(row=7, column=1)
tk.Checkbutton(root, text="C++", variable=cpp_var).grid(row=8, column=1)
tk.Checkbutton(root, text="Java", variable=java_var).grid(row=9, column=1)

submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=10, column=0, columnspan=2, pady=20)

result_label = tk.Label(root, text="", justify="left", font=("Arial", 10, "bold"))
result_label.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
