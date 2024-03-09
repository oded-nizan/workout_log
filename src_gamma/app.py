import sqlite3
import random
import string

admin_usernames = ["oded", "odednizan", "oded-nizan", "oded nizan"]
database_path = "database.db"


# Function to load database
def load_database(filename):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    conn.commit()
    conn.close()


# Function to create tables in the database
def create_tables():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        admin INTEGER
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS programs (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        program_name TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
                        id INTEGER PRIMARY KEY,
                        program_id INTEGER,
                        workout_name TEXT,
                        FOREIGN KEY (program_id) REFERENCES programs(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS exercises (
                        id INTEGER PRIMARY KEY,
                        workout_id INTEGER,
                        exercise_name TEXT,
                        sets INTEGER,
                        FOREIGN KEY (workout_id) REFERENCES workouts(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY,
                        exercise_id INTEGER,
                        log_number INTEGER,
                        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS log_sets (
                        id INTEGER PRIMARY KEY,
                        log_id INTEGER,
                        set_number INTEGER,
                        reps INTEGER,
                        weight INTEGER,
                        failure INTEGER,
                        FOREIGN KEY (log_id) REFERENCES logs(id)
                    )''')

    conn.commit()
    conn.close()


def is_admin_list(username):
    """Check if a username is in the admin list."""
    return username in admin_usernames


def generate_unique_id():
    """Generate a random unique ID for the user."""
    unique_id = ''.join(random.choices(string.digits, k=9))
    return unique_id


def add_user(username, password):
    """Add a new user to the database."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    admin = is_admin_list(username)
    cursor.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", (username, password, admin))
    conn.commit()
    conn.close()


def is_admin(username):
    """Check if a user is an admin."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT admin FROM users WHERE username = ?", (username,))
    admin = cursor.fetchone()
    conn.close()
    return admin[0] if admin else False


def change_admin_status(admin_username, username_to_change, new_admin_status):
    """Change the admin status of a user."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND admin = 1", (admin_username,))
    admin_user = cursor.fetchone()
    if not admin_user:
        print("You don't have permission to change admin status or admin does not exist.")
        conn.close()
        return

    cursor.execute("SELECT * FROM users WHERE username = ?", (username_to_change,))
    user_to_change = cursor.fetchone()
    if not user_to_change:
        print("User to change not found.")
        conn.close()
        return

    cursor.execute("UPDATE users SET admin = ? WHERE username = ?", (new_admin_status, username_to_change))
    conn.commit()
    print("Admin status updated successfully.")
    conn.close()


def view_user_info(admin_username):
    """View user information."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND admin = 1", (admin_username,))
    admin_user = cursor.fetchone()
    if not admin_user:
        print("You don't have permission to view user info or admin does not exist.")
        conn.close()
        return

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if not users:
        print("No users found.")
        conn.close()
        return

    print("List of Users:")
    for idx, user in enumerate(users, start=1):
        print(f"{idx}. {user[1]}")

    user_to_view = None
    while True:
        choice = input("Enter the number of the user whose info you wish to view (0 to exit): ")
        if choice == '0':
            conn.close()
            return
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(users):
            print("Invalid choice. Please enter a valid number.")
            continue
        user_to_view = users[int(choice) - 1]
        break

    if user_to_view:
        print("\nUser Info:")
        print("Username:", user_to_view[1])
        print("ID:", user_to_view[0])
        print("Admin:", "Yes" if user_to_view[3] else "No")
        print("Programs:", user_to_view[4])
    else:
        print("No user selected.")

    conn.close()


def owns_program(username, program_name):
    """Check if a user owns a program."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 
                      FROM programs p 
                      JOIN users u ON p.user_id = u.id 
                      WHERE u.username = ? AND p.program_name = ?''', (username, program_name))
    result = cursor.fetchone()
    conn.close()
    return True if result else False


def create_program(username, program_name):
    """Create a program."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO programs (user_id, program_name) VALUES (?, ?)", (user_id, program_name))
    conn.commit()
    conn.close()


def edit_program(admin_username):
    """Edit a program."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND admin = 1", (admin_username,))
    admin_user = cursor.fetchone()
    if not admin_user:
        print("You don't have permission to edit programs or admin does not exist.")
        conn.close()
        return

    cursor.execute("SELECT * FROM programs")
    programs = cursor.fetchall()

    if not programs:
        print("No programs found.")
        conn.close()
        return

    print("List of Programs:")
    for idx, program in enumerate(programs, start=1):
        print(f"{idx}. {program[1]}")

    program_to_edit = None
    while True:
        choice = input("Enter the number of the program you want to edit (0 to exit): ")
        if choice == '0':
            conn.close()
            return
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(programs):
            print("Invalid choice. Please enter a valid number.")
            continue
        program_to_edit = programs[int(choice) - 1]
        break

    if program_to_edit:
        print("\nProgram Info:")
        print("Program Name:", program_to_edit[1])
        print("Owner:", program_to_edit[2])
        print("Program Content:", program_to_edit[3])

        while True:
            exercise_to_edit = input("Enter the name of the exercise you want to edit (0 to exit): ")
            if exercise_to_edit == '0':
                break
            cursor.execute("SELECT * FROM exercises WHERE program_id = ? AND name = ?",
                           (program_to_edit[0], exercise_to_edit))
            exercise = cursor.fetchone()
            if not exercise:
                print("Exercise not found.")
                continue

            print("\nExercise Info:")
            print("Exercise Name:", exercise[2])
            print("Number of Sets:", exercise[3])

            new_sets = input("Enter the new number of sets: ")
            cursor.execute("UPDATE exercises SET sets = ? WHERE id = ?", (new_sets, exercise[0]))
            conn.commit()
            print("Exercise updated successfully.")
    else:
        print("No program selected.")

    conn.close()


def input_log_sets(set_count):
    """Input log sets."""
    log_sets = []
    for i in range(set_count):
        set_number = i + 1
        reps = int(input(f"Enter the amount of reps you did for set {set_number}: "))
        weight = int(input(f"Enter the weight you lifted for set {set_number}: "))
        failure = input(f"Did you fail on set {set_number}? (yes/no): ").lower() == "yes"
        log_sets.append({
            "set_number": set_number,
            "reps": reps,
            "weight": weight,
            "failure": failure
        })
    return log_sets


def log_data(username, program_name, exercise_name, log_number, log_sets):
    """Log data into the database."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM programs WHERE name = ?", (program_name,))
    program_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM exercises WHERE program_id = ? AND name = ?", (program_id, exercise_name))
    exercise_id = cursor.fetchone()[0]

    for log_set in log_sets:
        cursor.execute("INSERT INTO logs (user_id, program_id, exercise_id, log_number, set_number, reps, weight, "
                       "failure)"
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, program_id, exercise_id, log_number, log_set['set_number'],
                        log_set['reps'], log_set['weight'], log_set['failure']))

    conn.commit()
    conn.close()


def log_data_into_exercise(username):
    """Log data into an exercise."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        print("User not found.")
        conn.close()
        return

    cursor.execute("SELECT * FROM programs WHERE owner = ?", (username,))
    owned_programs = cursor.fetchall()

    cursor.execute("SELECT programs.* FROM programs INNER JOIN program_members "
                   "ON programs.id = program_members.program_id "
                   "WHERE program_members.username = ?", (username,))
    member_programs = cursor.fetchall()

    programs = owned_programs + member_programs

    if not programs:
        print("No programs found.")
        conn.close()
        return

    print("List of Programs:")
    for idx, program in enumerate(programs, start=1):
        print(f"{idx}. {program[1]}")

    program_to_log = None
    while True:
        choice = input("Enter the number of the program you want to log data into (0 to exit): ")
        if choice == '0':
            conn.close()
            return
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(programs):
            print("Invalid choice. Please enter a valid number.")
            continue
        program_to_log = programs[int(choice) - 1]
        break

    if program_to_log:
        print("\nProgram Info:")
        print("Program Name:", program_to_log[1])
        print("Owner:", program_to_log[2])
        print("Program Content:", program_to_log[3])

        cursor.execute("SELECT * FROM exercises WHERE program_id = ?", (program_to_log[0],))
        exercises = cursor.fetchall()
        if not exercises:
            print("No exercises found in this program.")
            conn.close()
            return

        print("\nList of Exercises:")
        for idx, exercise in enumerate(exercises, start=1):
            print(f"{idx}. {exercise[2]}")

        exercise_to_log = None
        while True:
            choice = input("Enter the number of the exercise you want to log data into (0 to exit): ")
            if choice == '0':
                conn.close()
                return
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(exercises):
                print("Invalid choice. Please enter a valid number.")
                continue
            exercise_to_log = exercises[int(choice) - 1]
            break

        if exercise_to_log:
            print("\nExercise Info:")
            print("Exercise Name:", exercise_to_log[2])
            print("Number of Sets:", exercise_to_log[3])

            while True:
                log_number = input("Enter log number (0 to exit): ")
                if log_number == '0':
                    conn.close()
                    return
                if not log_number.isdigit():
                    print("Log number must be a positive integer.")
                    continue
                log_sets = input_log_sets(exercise_to_log[3])
                log_data(username, program_to_log[1], exercise_to_log[2], int(log_number), log_sets)
                print("Workout log updated successfully.")
                choice = input("Do you want to log data into another log? (yes/no): ")
                if choice.lower() != 'yes':
                    conn.close()
                    return
        else:
            print("No exercise selected.")
    else:
        print("No program selected.")

    conn.close()


def sign_in(username, password):
    """Sign in with username and password."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and user[2] == password:
        print(f"Welcome back, {username}!")
        return user  # Return the user data
    else:
        print("Incorrect username or password.")
        return None


def menu(username):
    """Display the main menu."""
    print("\nMenu:")
    print("1. Create a program")
    print("2. Log data into a program")
    print("3. Edit a program")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        program_name = input("Enter program name: ")
        create_program(username, program_name)
    elif choice == '2':
        log_data_into_exercise(username)
    elif choice == '3':
        edit_program(username)
    elif choice == '4':
        print("Exiting program.")
    else:
        print("Invalid choice. Please enter a number from 1 to 4.")


def main():
    """Main function."""
    load_database(database_path)
    create_tables()

    while True:
        print("\nWelcome to the Fitness Tracker!")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        user = sign_in(username, password)
        if user:
            menu(username)
            break
        else:
            print("Invalid username or password. Please try again.")


if __name__ == "__main__":
    main()
