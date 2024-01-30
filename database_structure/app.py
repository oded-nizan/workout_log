# imports
import json
import random
import string


# global variables
database_path = "database.json"


def load_database(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def save_database(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def get_user_by_username(database, username):
    for user in database['users']:
        if user['username'] == username:
            return user
    return None


def get_program_by_name(user, program_name):
    for program in user['programs']:
        if program['program_name'] == program_name:
            return program
    return None


def get_workout_by_name(program, workout_name):
    for workout in program['program_split']:
        if workout['workout_name'] == workout_name:
            return workout
    return None


def add_user(database, user_data):
    if user_data in database['users']:
        print("User already exists")
        return
    database['users'].append(user_data)
    save_database(database, database_path)


def generate_unique_id(database):
    # Generate a random unique ID
    while True:
        new_id = ''.join(random.choices(string.digits, k=9))
        if not any(user['id'] == new_id for user in database['users']):
            return new_id


def is_strong_password(password):
    # Check if password is strong enough (e.g., length > 6)
    return len(password) > 6


def is_unique_username(database, username):
    # Check if username is unique
    return not any(user['username'] == username for user in database['users'])


def create_user(database, username, password):
    new_user = {
        "username": username,
        "id": generate_unique_id(database),
        "password": password,
        "admin": False,
        "programs": []
    }
    add_user(database, new_user)
    print("User created successfully")
    save_database(database, database_path)


def input_new_user(database):
    while True:
        username = input("Enter your username: ")
        if is_unique_username(database, username):
            break
        print("Username already exists. Please choose another.")

    while True:
        password = input("Enter your password: ")
        if is_strong_password(password):
            break
        print("Password should be at least 8 characters long")

    create_user(database, username, password)


def update_workout_log(database, username, program_name, workout_name, exercise_name, log_number, log_sets):
    user = get_user_by_username(database, username)
    if user:
        for program in user['programs']:
            if program['program_name'] == program_name:
                for workout in program['program_split']:
                    if workout['workout_name'] == workout_name:
                        for exercise in workout['exercises']:
                            if exercise['exercise_name'] == exercise_name:
                                for log in exercise['exercise_log']:
                                    if log['log_number'] == log_number:
                                        log['log_sets'] = log_sets
                                        save_database(database, database_path)
                                        return True
    save_database(database, database_path)
    return False


def create_exercise():
    exercise_name = input("Enter exercise name: ")
    sets = int(input("Enter number of sets: "))
    return {
        "exercise_name": exercise_name,
        "sets": sets,
        "exercise_log": []
    }


def create_workout():
    workout_name = input("Enter workout name: ")
    exercise_count = int(input("Enter number of exercises for this workout: "))
    exercises = [create_exercise() for _ in range(exercise_count)]
    return {
        "workout_name": workout_name,
        "exercises": exercises
    }


def create_program():
    program_name = input("Enter program name: ")
    workout_count = int(input("Enter number of workouts for this program: "))
    program_split = [create_workout() for _ in range(workout_count)]
    return {
        "program_name": program_name,
        "program_split": program_split
    }


def create_program_without_logs(database, username):
    user = get_user_by_username(database, username)
    if not user:
        print("User not found.")
        return

    program_data = create_program()
    user["programs"].append(program_data)
    print("Program created successfully.")
    save_database(database, database_path)


def input_log_sets(set_count):
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


def check_program_name_input(program_name, user):
    return next((program for program in user['programs'] if program['program_name'] == program_name), None)


def input_program_name(user):
    while True:
        program_name = input("Enter program name: ")
        program_exists = check_program_name_input(program_name, user)
        if program_exists:
            break
        print("Program not found")
    return program_name


def check_workout_name_input(workout_name, program):
    return next((workout for workout in program['program_split'] if workout['workout_name'] == workout_name), None)


def input_workout_name(program):
    while True:
        workout_name = input("Enter workout name: ")
        if check_workout_name_input(workout_name, program):
            break
        print("Workout doesn't exist")
    return workout_name


def check_exercise_name_input(exercise_name, workout):
    return next((exercise for exercise in workout['exercises'] if exercise['exercise_name'] == exercise_name), None)


def input_exercise_name(workout):
    while True:
        exercise_name = input("Enter exercise name: ")
        if check_exercise_name_input(exercise_name, workout):
            break
        print("Exercise doesn't exist")
    return exercise_name


def input_workout_log_data(user):
    program_name = input_program_name(user)
    program = get_program_by_name(user, program_name)
    workout_name = input_workout_name(program)
    workout = get_workout_by_name(program, workout_name)
    exercise_name = input_exercise_name(workout)
    log_number = int(input("Enter log number: "))
    set_count = int(input("Enter number of sets: "))
    return program_name, workout_name, exercise_name, log_number, set_count


def add_workout_log(database, username):
    user = get_user_by_username(database, username)
    if not user:
        print("User not found.")
        return

    program_name, workout_name, exercise_name, log_number, set_count = input_workout_log_data(user)
    log_sets = input_log_sets(set_count)

    if update_workout_log(database, username, program_name, workout_name, exercise_name, log_number, log_sets):
        print("Workout log updated successfully.")
    else:
        print("Failed to update workout log. Please check your input.")


def main():
    database = load_database(database_path)

    # Add a new user
    new_user = {
        "username": "john",
        "id": 100000002,
        "password": "password123",
        "admin": False,
        "programs": []
    }
    add_user(database, new_user)


if __name__ == '__main__':
    main()
