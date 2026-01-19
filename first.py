import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

# Helper to find files in bundled EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

USERS_FILE = resource_path("users.json")
HISTORY_FILE = resource_path("history.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

users = load_users()
history = load_history()
current_user = None
habit_vars = {}

window = ttk.Window(
    title="Habit Tracker Application",
    themename="flatly",
    size=(1000, 700)
)

# ==================== LOGIN FRAME ====================
frame1 = ttk.Frame(window)
frame1.pack(expand=True)

ttk.Label(
    frame1,
    text="Habit Tracker",
    font=("Arial", 28, "bold")
).pack(pady=30)

ttk.Label(
    frame1,
    text="Build Better Habits, One Day at a Time",
    font=("Arial", 11),
    bootstyle="secondary"
).pack(pady=(0, 30))

login_container = ttk.Frame(frame1)
login_container.pack(pady=10)

ttk.Label(
    login_container,
    text="Username:",
    font=("Arial", 12)
).grid(row=0, column=0, sticky="w", pady=10, padx=(0, 10))

username_entry = ttk.Entry(login_container, width=30)
username_entry.grid(row=0, column=1, pady=10)

ttk.Label(
    login_container,
    text="Password:",
    font=("Arial", 12)
).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 10))

password_entry = ttk.Entry(login_container, width=30, show="*")
password_entry.grid(row=1, column=1, pady=10)

button_frame = ttk.Frame(frame1)
button_frame.pack(pady=30)

ttk.Button(
    button_frame,
    text="Login",
    bootstyle=PRIMARY,
    width=15,
    command=lambda: login()
).pack(side="left", padx=10)

ttk.Button(
    button_frame,
    text="Sign Up",
    bootstyle=SUCCESS,
    width=15,
    command=lambda: show_signup_page()
).pack(side="left", padx=10)
def show_graph_window():
    graph_win = ttk.Toplevel(window)
    graph_win.title("Habit Graph")
    graph_win.geometry("900x500")
    Graph(graph_win) 

# ==================== SIGNUP FRAME ====================
frame_signup = ttk.Frame(window)
name_entry = None
age_entry = None
signup_username_entry = None
signup_password_entry = None

def show_signup_page():
    global name_entry, age_entry, signup_username_entry, signup_password_entry
    
    frame1.pack_forget()
    frame_signup.pack(expand=True)
    
    for widget in frame_signup.winfo_children():
        widget.destroy()
    
    ttk.Label(
        frame_signup,
        text="Create Your Account",
        font=("Arial", 26, "bold")
    ).pack(pady=30)
    
    ttk.Label(
        frame_signup,
        text="Join us and start building amazing habits",
        font=("Arial", 11),
        bootstyle="secondary"
    ).pack(pady=(0, 30))
    
    signup_container = ttk.Frame(frame_signup)
    signup_container.pack(pady=10)
    
    ttk.Label(
        signup_container,
        text="Full Name:",
        font=("Arial", 12)
    ).grid(row=0, column=0, sticky="w", pady=12, padx=(0, 15))
    
    name_entry = ttk.Entry(signup_container, width=35)
    name_entry.grid(row=0, column=1, pady=12)
    
    ttk.Label(
        signup_container,
        text="Age:",
        font=("Arial", 12)
    ).grid(row=1, column=0, sticky="w", pady=12, padx=(0, 15))
    
    age_entry = ttk.Entry(signup_container, width=35)
    age_entry.grid(row=1, column=1, pady=12)
    
    ttk.Label(
        signup_container,
        text="Username:",
        font=("Arial", 12)
    ).grid(row=2, column=0, sticky="w", pady=12, padx=(0, 15))
    
    signup_username_entry = ttk.Entry(signup_container, width=35)
    signup_username_entry.grid(row=2, column=1, pady=12)
    
    ttk.Label(
        signup_container,
        text="Password:",
        font=("Arial", 12)
    ).grid(row=3, column=0, sticky="w", pady=12, padx=(0, 15))
    
    signup_password_entry = ttk.Entry(signup_container, width=35, show="*")
    signup_password_entry.grid(row=3, column=1, pady=12)
    
    btn_container = ttk.Frame(frame_signup)
    btn_container.pack(pady=30)
    
    ttk.Button(
        btn_container,
        text="Create Account",
        bootstyle=SUCCESS,
        width=18,
        command=lambda: complete_signup()
    ).pack(side="left", padx=10)
    
    ttk.Button(
        btn_container,
        text="Back to Login",
        bootstyle=SECONDARY,
        width=18,
        command=lambda: back_to_login()
    ).pack(side="left", padx=10)

def back_to_login():
    frame_signup.pack_forget()
    frame1.pack(expand=True)

def complete_signup():
    global current_user
    
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    username = signup_username_entry.get().strip()
    password = signup_password_entry.get().strip()
    
    if not name or not age or not username or not password:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    
    if not age.isdigit() or int(age) < 5 or int(age) > 120:
        messagebox.showerror("Error", "Please enter a valid age!")
        return
    
    if username in users:
        messagebox.showerror("Error", "Username already exists!")
        return
    
    users[username] = {
        "password": password,
        "name": name,
        "age": int(age),
        "habits": []
    }
    
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
    
    current_user = username
    messagebox.showinfo("Success", f"Welcome aboard, {name}!")
    show_habit_setup()

def login():
    global current_user
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password!")
        return
    
    if username in users and users[username]["password"] == password:
        current_user = username
        if users[username]["habits"]:
            show_tracker()
        else:
            show_habit_setup()
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# ==================== HABIT SETUP FRAMES ====================
frame2 = ttk.Frame(window)

def show_habit_setup():
    frame1.pack_forget()
    frame_signup.pack_forget()
    frame2.pack(expand=True)
    
    for widget in frame2.winfo_children():
        widget.destroy()

    ttk.Label(
        frame2,
        text="Let's Set Up Your Habits",
        font=("Arial", 20, "bold")
    ).pack(pady=30)
    
    ttk.Label(
        frame2,
        text="How many habits do you want to track?",
        font=("Arial", 13)
    ).pack(pady=15)
    
    global habit_count_entry
    habit_count_entry = ttk.Entry(frame2, width=15, font=("Arial", 12))
    habit_count_entry.pack(pady=15)
    
    ttk.Label(
        frame2,
        text="(Choose between 1 and 6 habits)",
        font=("Arial", 10),
        bootstyle="secondary"
    ).pack(pady=5)
    
    ttk.Button(
        frame2,
        text="Next",
        bootstyle=PRIMARY,
        width=18,
        command=lambda: create_habit_inputs()
    ).pack(pady=25)

frame3 = ttk.Frame(window)
habit_entries = []

def create_habit_inputs():
    if not habit_count_entry.get().isdigit():
        messagebox.showerror("Error", "Enter a valid number!")
        return
    
    count = int(habit_count_entry.get())
    
    if count < 1 or count > 6:
        messagebox.showerror("Error", "Enter a number between 1 and 6!")
        return
    
    frame2.pack_forget()
    frame3.pack(expand=True)
    
    for widget in frame3.winfo_children():
        widget.destroy()
    
    ttk.Label(
        frame3,
        text="Name Your Habits",
        font=("Arial", 20, "bold")
    ).pack(pady=25)
    
    ttk.Label(
        frame3,
        text="Give each habit a clear, specific name",
        font=("Arial", 11),
        bootstyle="secondary"
    ).pack(pady=(0, 20))
    
    habit_entries.clear()
    
    for i in range(count):
        habit_frame = ttk.Frame(frame3)
        habit_frame.pack(pady=8, padx=50, fill="x")
        
        ttk.Label(
            habit_frame,
            text=f"Habit {i+1}:",
            font=("Arial", 12, "bold"),
            width=10
        ).pack(side="left", padx=(0, 10))
        
        entry = ttk.Entry(habit_frame, width=40, font=("Arial", 11))
        entry.pack(side="left", fill="x", expand=True)
        habit_entries.append(entry)
    
    ttk.Button(
        frame3,
        text="Start Tracking",
        bootstyle=SUCCESS,
        width=20,
        command=lambda: save_habits()
    ).pack(pady=30)

def save_habits():
    habits = []
    for entry in habit_entries:
        if entry.get().strip():
            habits.append(entry.get().strip())
    
    if not habits:
        messagebox.showerror("Error", "Please enter at least one habit!")
        return
    
    users[current_user]["habits"] = habits
    
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
    
    if current_user not in history:
        history[current_user] = {}
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
    
    show_tracker()

# ==================== TRACKER FRAME ====================
frame4 = ttk.Frame(window)

def calculate_streak(habit_name):
    """Calculate current streak for a habit (resets to 0 if any day is missed)"""
    if current_user not in history:
        return 0
    
    user_data = history[current_user]
    if not user_data:
        return 0
    
    sorted_dates = sorted(user_data.keys(), reverse=True)
    
    streak = 0
    today = date.today()
    
    for i, date_str in enumerate(sorted_dates):
        check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        expected_date = today - timedelta(days=i)
        
        if check_date != expected_date:
            break
        
        if user_data[date_str].get(habit_name) == "Yes":
            streak += 1
        else:
            break
    
    return streak
def Graph(parent):
    user_data = history.get(current_user, {})
    habits = users[current_user]["habits"]

    if not user_data:
        return

    dates = sorted(user_data.keys())[-21:]

    cell_text = []
    for d in dates:
        row = [d]
        for h in habits:
            row.append("✔" if user_data[d].get(h) == "Yes" else "✖")
        cell_text.append(row)

    col_labels = ["Dates"] + habits

    fig, ax = plt.subplots(figsize=(len(habits)*1.5 + 2, len(dates)*0.5))
    ax.axis('off')

    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def show_tracker():
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame_signup.pack_forget()
    frame4.pack(expand=True, fill="both")
    
    for widget in frame4.winfo_children():
        widget.destroy()
    
    header = ttk.Frame(frame4)
    header.pack(fill="x", pady=15, padx=20)
    
    user_name = users[current_user].get("name", current_user)
    
    ttk.Label(
        header,
        text=f"Welcome back, {user_name}!",
        font=("Arial", 18, "bold")
    ).pack(anchor="w")
    
    ttk.Label(
        header,
        text=f"Today: {date.today().strftime('%A, %B %d, %Y')}",
        font=("Arial", 11),
        bootstyle="secondary"
    ).pack(anchor="w", pady=(5, 0))
    
    main_frame = ttk.Frame(frame4)
    main_frame.pack(fill="both", expand=True, padx=30, pady=10)
    
    today = str(date.today())
    today_data = history.get(current_user, {}).get(today, {})
    
    habit_vars.clear()
    habits = users[current_user]["habits"]
    
    for h in habits:
        habit_vars[h] = ttk.BooleanVar(value=today_data.get(h) == "Yes")
        
        habit_container = ttk.Frame(main_frame)
        habit_container.pack(fill="x", pady=10)
        
        ttk.Checkbutton(
            habit_container,
            text=h,
            variable=habit_vars[h],
            bootstyle="success-round-toggle"
        ).pack(anchor="w")
    
    button_container = ttk.Frame(frame4)
    button_container.pack(pady=20, side="bottom")
    
    ttk.Button(
        button_container,
        text="Save Today",
        bootstyle=PRIMARY,
        width=15,
        command=save_today
    ).pack(side="left", padx=8)
    
    ttk.Button(
        button_container,
        text="Dashboard",
        bootstyle=INFO,
        width=15,
        command=show_dashboard
    ).pack(side="left", padx=8)
    
    ttk.Button(
        button_container,
        text="Logout",
        bootstyle=DANGER,
        width=15,
        command=logout
    ).pack(side="left", padx=8)

    ttk.Button(
        button_container,
        text="Graph",
        bootstyle=DANGER,
        width=15,
        command=show_graph_window
    ).pack(side="left", padx=8)

def save_today():
    today = str(date.today())
    
    final_data = {}
    habits = users[current_user]["habits"]
    
    completed_habits = []
    for h in habits:
        final_data[h] = "Yes" if habit_vars[h].get() else "No"
        
        if final_data[h] == "Yes":
            current_streak = calculate_streak(h)
            if current_streak + 1 == 21:
                completed_habits.append(h)
    
    if current_user not in history:
        history[current_user] = {}
    
    history[current_user][today] = final_data
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
    
    messagebox.showinfo("Saved", "Today's habits saved successfully!")
    
    for habit in completed_habits:
        messagebox.showinfo(
            "Congratulations!",
            f"You just gained a new habit!\n\n'{habit}'\n\n21 days completed!"
        )
    show_tracker()
def show_dashboard():
    dash_win = ttk.Toplevel(window)
    dash_win.title("Habit Dashboard")
    dash_win.geometry("900x700")
    
    user_data = history.get(current_user, {})
    habits = users[current_user]["habits"]
    user_name = users[current_user].get("name", current_user)
    user_age = users[current_user].get("age", "N/A")
    
    # Header Section
    header_frame = ttk.Frame(dash_win)
    header_frame.pack(fill="x", padx=30, pady=20)
    
    ttk.Label(
        header_frame,
        text="Habit Dashboard",
        font=("Arial", 24, "bold")
    ).pack(anchor="w")
    
    ttk.Separator(dash_win, orient="horizontal").pack(fill="x", padx=30, pady=10)
    
    # User Info Section
    info_frame = ttk.Labelframe(dash_win, text="User Information", padding=20)
    info_frame.pack(fill="x", padx=30, pady=10)
    
    info_grid = ttk.Frame(info_frame)
    info_grid.pack(fill="x")
    
    ttk.Label(
        info_grid,
        text="Name:",
        font=("Arial", 12, "bold")
    ).grid(row=0, column=0, sticky="w", padx=10, pady=8)
    
    ttk.Label(
        info_grid,
        text=user_name,
        font=("Arial", 12)
    ).grid(row=0, column=1, sticky="w", padx=10, pady=8)
    
    ttk.Label(
        info_grid,
        text="Age:",
        font=("Arial", 12, "bold")
    ).grid(row=0, column=2, sticky="w", padx=30, pady=8)
    
    ttk.Label(
        info_grid,
        text=str(user_age),
        font=("Arial", 12)
    ).grid(row=0, column=3, sticky="w", padx=10, pady=8)
    
    ttk.Label(
        info_grid,
        text="Total Days Tracked:",
        font=("Arial", 12, "bold")
    ).grid(row=1, column=0, sticky="w", padx=10, pady=8)
    
    ttk.Label(
        info_grid,
        text=str(len(user_data)),
        font=("Arial", 12)
    ).grid(row=1, column=1, sticky="w", padx=10, pady=8)
    
    # Habits Section
    habits_frame = ttk.Labelframe(dash_win, text="Tracked Habits", padding=20)
    habits_frame.pack(fill="x", padx=30, pady=10)
    
    for idx, h in enumerate(habits, 1):
        ttk.Label(
            habits_frame,
            text=f"{idx}. {h}",
            font=("Arial", 11)
        ).pack(anchor="w", pady=3)
    
    # Progress Section
    progress_frame = ttk.Labelframe(dash_win, text="21-Day Challenge Progress", padding=20)
    progress_frame.pack(fill="both", expand=True, padx=30, pady=10)
    
    for h in habits:
        current_streak = calculate_streak(h)
        completed_days = sum(1 for day_data in user_data.values() if day_data.get(h) == "Yes")
        
        habit_progress_frame = ttk.Frame(progress_frame)
        habit_progress_frame.pack(fill="x", pady=15)
        
        # Habit name and stats
        label_frame = ttk.Frame(habit_progress_frame)
        label_frame.pack(fill="x")
        
        ttk.Label(
            label_frame,
            text=h,
            font=("Arial", 12, "bold")
        ).pack(side="left")
        
        ttk.Label(
            label_frame,
            text=f"Current Streak: {current_streak}/21 days",
            font=("Arial", 11),
            bootstyle=SUCCESS if current_streak > 0 else "secondary"
        ).pack(side="right", padx=10)
        
        ttk.Label(
            label_frame,
            text=f"Total Completed: {completed_days} days",
            font=("Arial", 11),
            bootstyle=INFO
        ).pack(side="right")
        
        # Progress bar
        progress = ttk.Progressbar(
            habit_progress_frame,
            length=700,
            maximum=21,
            value=current_streak,
            bootstyle=SUCCESS
        )
        progress.pack(fill="x", pady=(10, 0))
        
        # Percentage label
        percentage = (current_streak / 21) * 100
        ttk.Label(
            habit_progress_frame,
            text=f"{percentage:.0f}%",
            font=("Arial", 10),
            bootstyle="secondary"
        ).pack(anchor="e", pady=(2, 0))
    
    # Close button
    ttk.Button(
        dash_win,
        text="Close",
        bootstyle=PRIMARY,
        width=15,
        command=dash_win.destroy
    ).pack(pady=20)

def logout():
    global current_user
    current_user = None
    frame4.pack_forget()
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")
    frame1.pack(expand=True)

window.mainloop() 