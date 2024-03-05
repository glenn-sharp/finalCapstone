# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.
# Create tasks.txt if it doesn't exist

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# function to register new user and write to txt file
def reg_user():
    # - Request input of a new username and check if username already exists
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists.")
        return
    # - Request input of a new password
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        # - If they are the same, add them to the user.txt file,
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    # - Otherwise you present a relevant message.        
    else:
        print("Passwords do not match")

# function to create task for user including title/due date/description and write to txt file
def add_task():
    task_username = input("Name of person assigned to task: ")
    # error control if user doesnt exist
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    # get current date        
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    # write task to file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# function that displays users tasks
def print_task_details(task):
    disp_str = f"Task: {task['title']}\n"
    disp_str += f"Assigned to: {task['username']}\n"
    disp_str += f"Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Description:\n{task['description']}\n"
    disp_str += f"Completed: {'Yes' if task['completed'] else 'No'}\n"
    print(disp_str)

# function to edit users tasks
def edit_task(task):
    print("Select what you want to edit:")
    print("1. Task Assignee")
    print("2. Due Date")
    edit_choice = input("Enter your choice (1/2): ")
    if edit_choice == "1":
        new_assignee = input("Enter the new assignee: ")
        task['username'] = new_assignee
        print("Assignee updated successfully.")
    elif edit_choice == "2":
        while True:
            try:
                new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                print("Due date updated successfully.")
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified (YYYY-MM-DD).")
    else:
        print("Invalid choice.")

# function that views all tasks and numbers tasks in order
def view_all():
    for i, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            disp_str = f"Task {i}:\n"
            disp_str += f"Title: {t['title']}\n"
            disp_str += f"Assigned to: {t['username']}\n"
            disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

# function that views users tasks and provides options to edit task details
def view_mine():
    user_tasks = [t for t in task_list if t['username'] == curr_user]
    for task_index, t in enumerate(user_tasks, start=1):
        disp_str = f"Task {task_index}:\n"
        disp_str += f"Title: {t['title']}\n"
        disp_str += f"Assigned to: {t['username']}\n"
        disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description:\n{t['description']}\n"
        disp_str += f"Completed: {'Yes' if t['completed'] else 'No'}\n"
        print(disp_str)
    print("Enter the index of the task you want to select, or enter -1 to return to the main menu.")
    selected_task_index = int(input("Enter your choice: "))
    if selected_task_index == -1:
        return 
    elif selected_task_index < 1 or selected_task_index > len(user_tasks):
        print("Invalid task index. Please enter a valid index.")
        return
    else:
        selected_task = user_tasks[selected_task_index - 1]
        print("\nSelected Task:")
        print_task_details(selected_task)
        print("Do you want to:")
        print("1. Mark this task as complete")
        print("2. Edit this task")
        edit_choice = input("Enter your choice: ")
        if edit_choice == "1":
            selected_task['completed'] = True
            print("Task marked as complete.")
        elif edit_choice == "2":
            edit_task(selected_task) 
        else:
            print("Invalid choice.")
# function that generates user reports and writes to txt file 
def generate_user_report():
    total_users = len(username_password.keys())
    total_tasks = len(task_list)
    user_task_counts = {}
    for user in username_password.keys():
        user_task_counts[user] = sum(1 for t in task_list if t['username'] == user)
    with open("user_overview.txt", "w") as report_file:
        report_file.write("USER OVERVIEW REPORT\n")
        report_file.write("-----------------------------------\n")
        report_file.write(f"Total number of users: {total_users}\n")
        report_file.write(f"Total number of tasks: {total_tasks}\n")
        report_file.write("-----------------------------------\n")
        report_file.write("Tasks per user:\n")
        for user, task_count in user_task_counts.items():
            report_file.write(f"{user}: {task_count}\n")
        report_file.write("-----------------------------------\n")
    print("User overview report has been saved to user_overview.txt")

# function that generates task reports and writes to file 
def generate_report():
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < date.today())
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100
    with open("task_overview.txt", "w") as report_file:
        report_file.write("TASK OVERVIEW REPORT\n")
        report_file.write("-----------------------------------\n")
        report_file.write(f"Total number of tasks: {total_tasks}\n")
        report_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        report_file.write(f"Total number of incomplete tasks: {incomplete_tasks}\n")
        report_file.write(f"Total number of tasks overdue: {overdue_tasks}\n")
        report_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
        report_file.write(f"Percentage of tasks overdue: {overdue_percentage:.2f}%\n")
        report_file.write("-----------------------------------\n")
        report_file.write("Task Details:\n")
        # numbers each task in order of appearance
        for i, task in enumerate(task_list, start=1):
            report_file.write(f"Task {i}:\n")
            report_file.write(f"Title: {task['title']}\n")
            report_file.write(f"Assigned to: {task['username']}\n")
            report_file.write(f"Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n")
            report_file.write(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")
            report_file.write(f"Description: {task['description']}\n")
            report_file.write(f"Completed: {'Yes' if task['completed'] else 'No'}\n")
            report_file.write("-----------------------------------\n")
    print("Task overview report has been saved to task_overview.txt")

# function that marks tasks as complete and writes to file
def mark_task_complete():
    task_index = int(input("Enter the index of the task to mark as complete: "))
    if task_index < 1 or task_index > len(task_list):
        print("Invalid task index")
        return
    task_list[task_index - 1]['completed'] = True
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task marked as complete.")

# function that displays user statistics when logged in as admin and writes to file
def display_statistics():
    if curr_user == 'admin':
        total_users = len(username_password)
        total_tasks = len(task_list)
        print("-----------------------------------")
        print(f"Number of users: \t\t {total_users}")
        print(f"Number of tasks: \t\t {total_tasks}")
        print("-----------------------------------")
    else:
        print("This option is only available to Admin.")
username_password = {}
task_list = []
curr_user = None
# If no user.txt file, write one with a default account
if os.path.exists("user.txt"):
    with open("user.txt", "r") as user_file:
        for line in user_file:
            username, password = line.strip().split(";")
            username_password[username] = password
# Create tasks.txt if it doesn't exist
if os.path.exists("tasks.txt"):
    with open("tasks.txt", "r") as task_file:
        for line in task_file:
            task_attrs = line.strip().split(";")
            if len(task_attrs) >= 6:
                due_date = datetime.strptime(task_attrs[3], DATETIME_STRING_FORMAT)
                assigned_date = datetime.strptime(task_attrs[4], DATETIME_STRING_FORMAT)
                completed = True if task_attrs[5] == "Yes" else False
                task_list.append({
                    "username": task_attrs[0],
                    "title": task_attrs[1],
                    "description": task_attrs[2],
                    "due_date": due_date,
                    "assigned_date": assigned_date,
                    "completed": completed
                })
            else:
                print("Invalid task format in tasks file.")

# presenting the menu to the user
while True:
    if curr_user is None:
        print("\nWelcome to the Task Manager")
        print("1. Register")
        print("2. Login")
        choice = input("Choose option: ")
        if choice == "1":
            reg_user()
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            if username in username_password and username_password[username] == password:
                curr_user = username
            else:
                print("Invalid username or password")
        else:
            print("Invalid choice")
    else:
        print("\nWelcome " + curr_user)
        print("1. Add task")
        print("2. View all tasks")
        print("3. View my tasks")
        print("4. Generate reports")
        print("5. Display Statistics")
        print("6. Log out")
        choice = input("Choose option: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_all()
        elif choice == "3":
            view_mine()
        elif choice == "4":
            print("1. Generate task overview report")
            print("2. Generate user overview report")
            report_choice = input("Choose report type: ")
            if report_choice == "1":
                generate_report()
            elif report_choice == "2":
                generate_user_report()
            else:
                print("Invalid report type")
        elif choice == '5':
            display_statistics()
        elif choice == "6":
            curr_user = None
        else:
            print("Invalid choice")