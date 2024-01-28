# imports
import json
import os


def welcome():
    # ask if user is new
    while True:
        new_user = input("Welcome! Are you a new user? (y/n): ")
        if new_user == "y" or new_user == "n":
            break
        print("Invalid input.")
    # translate answer to later use in main
    if new_user == "y":
        return False
    return True


def user_exists(username):
    # open the file and load into a dictionary
    with open("users.json", "r") as f:
        users_data = json.load(f)
    username_list = users_data["users"]
    for user_name in username_list:
        if user_name["username"] == username:
            return True
    return False


def login():
    # input username and check if it is in the file
    username = input("Enter username: ")
    # open the file and load into a dictionary
    with open("users.json", "r") as f:
        users_data = json.load(f)
    if user_exists(username):
        # if username exists, check password
        password = input("Enter password: ")
        # compare to real password
        users_list = users_data["users"]
        real_password = ""
        for user_name in users_list:
            if user_name["username"] == username:
                real_password = user_name["password"]
        if password != real_password:
            print("Incorrect password")
            return False
        else:
            print("Successfully logged in")
            return True
    # if username doesn't exist
    else:
        print("Invalid username")
        return False


def varify_user(username):
    # open the file and load into a dictionary
    with open("users.json", "r") as f:
        users_data = json.load(f)
    password = input("Enter password: ")
    # compare to real password
    users_list = users_data["users"]
    real_password = ""
    for user_name in users_list:
        if user_name["username"] == username:
            real_password = user_name["password"]
    if password != real_password:
        print("Incorrect password")
        return False
    else:
        print("Successfully logged in")
        return True


def create_user():
    # load data from json file
    with open("users.json", "r") as f:
        users_data = json.load(f)
    username_list = users_data.keys()
    # get input username
    while True:
        username = input("Enter username: ")
        if username not in username_list:
            break
        print("Username already exists.")
    # password requirements
    print("Password must be at least 8 characters.")
    while True:
        password = input("Enter a password: ")
        if len(password) >= 8:
            break
        else:
            print("Invalid password")
    # since username doesn't exist this will create a new key-value pair
    users_data.setdefault(username, password)
    with open("users.json", "w") as f:
        json.dump(users_data, f)


def edit_program(username):
    # if file exists edit program
    while True:
        program_name = input("Enter program name: ")
        program_name = username + '_' + program_name + '.json'
        file_exists = os.path.exists(program_name)
        if file_exists:
            break
        print("Program doesn't exists")

    # check if program is owed by user
    with open(program_name, "r") as f:
        program_data = json.load(f)
    if username == program_data["user"]:
        varify = varify_user(username)
        if varify:
            pass
        else:
            print("You do not have permission, you will be restricted")
            return
    else:
        return

    # edit program
    while True:
        while True:
            action = input("Do you wish to add and exercise, change one or delete one? (add/change/delete): ")
            if action == "add" or action == "change" or action == "delete":
                break
            print("Invalid action")
        match action:
            case "add":
                add_exercise(program_name)
            case "change":
                change_exercise(program_name)
            case "delete":
                delete_exercise(program_name)
            case _:
                print("Something went wrong ;(")
        continue_actions = input("If you wish to continue to edit this program enter True: ")
        if not continue_actions:
            break


def add_exercise(program_name):
    with open(program_name, "r") as f:
        program_data = json.load(f)
    exercises = program_data["exercises"]
    name = input("Enter the name of the exercise: ")
    sets = int(input("Enter the number of sets: "))
    exercise = {
        "name": name,
        "sets": sets
    }
    exercises.appand(exercise)
    program_data["exercises"] = exercises
    with open(program_name, "w") as f:
        json.dump(program_data, f)


def change_exercise(program_name):
    with open(program_name, "r") as f:
        program_data = json.load(f)
    exercises = program_data["exercises"]
    new_exercise = {}
    for exercise in exercises:
        print(exercise["name"])
        edit = input("Is this the exercise you wish to edit? (y/n): ")
        if edit == "y":
            name = input("Enter the name of the exercise: ")
            sets = int(input("Enter the number of sets: "))
            new_exercise = {
                "name": name,
                "sets": sets
            }
            break
    if new_exercise == {}:
        print("You didn't select any exercise, abort.")
    else:
        exercises.appand(new_exercise)
        program_data["exercises"] = exercises
        with open(program_name, "w") as f:
            json.dump(program_data, f)


def delete_exercise(program_name):
    with open(program_name, "r") as f:
        program_data = json.load(f)
    exercises = program_data["exercises"]
    for exercise in exercises:
        print(exercise["name"])
        delete = input("Is this the exercise you wish to edit? (y/n): ")
        if delete == "y":
            exercises.remove(exercise)
            break
    program_data["exercises"] = exercises
    with open(program_name, "w") as f:
        json.dump(program_data, f)


def create_program(username):
    program_name = input("Enter program name: ")
    program_name = username + '_' + program_name + '.json'
    exercises = []
    while True:
        name = input("Enter exercise name: (n if you wish to stop entering): ")
        if name == "n":
            break
        sets = int(input("Enter number of sets: "))
        exercise = {
            "name": name,
            "sets": sets
        }
        exercises.append(exercise)
    program_data = {
        "exercises": exercises
    }
    with open(program_name, "w") as f:
        json.dump(program_data, f)


def print_program(username):
    # if file exists print program
    while True:
        program_name = input("Enter program name: ")
        program_name = username + '_' + program_name + '.json'
        file_exists = os.path.exists(program_name)
        if file_exists:
            break
        print("Program doesn't exists")

    # check if program is owed by user
    with open(program_name, "r") as f:
        program_data = json.load(f)
    if username == program_data["user"]:
        varify = varify_user(username)
        if varify:
            pass
        else:
            print("You do not have permission, you will be restricted")
            return
    else:
        return

    # print program
    print("The program " + program_name + "'s details will be printed: ")
    exercises = program_data["exercises"]
    for i in range(len(exercises)):
        exercise = exercises[i]
        print("Exercise number ", i, "name: " + exercise["name"] + "sets: ", exercise["sets"])


def user_options(username):
    print(
        "If you wish to make changes to a current program enter 0, if you wish to create a new program enter 1, "
        "if you wish to enter data to a program enter 2, if you wish to print a program enter 3: ")
    while True:
        choice = input("Enter your choice: ")
        if choice == 1 or choice == 0:
            break
        print("Invalid choice.")
    if choice == 0:
        edit_program(username)
    elif choice == 1:
        create_program(username)
    elif choice == 2:
        print("You choose to enter data to a program: ")
        # TODO: enter_data(username)
    else:
        print("You choose to print a program")
        # TODO: print_program(username)


def main():
    # check if user is new and login or create user accordingly
    user_exists_start = welcome()
    if user_exists_start:
        logged_in = login()
        if not logged_in:
            print("You should attempt to login again.")
    else:
        print("We shall start creating your profile!")
        create_user()
    while True:
        username = input("Enter your username: ")
        if user_exists(username):
            break
        else:
            print("Incorrect username")
    user_options(username)
# TODO: adapt form exercise list method to days per week with lists per day

if __name__ == '__main__':
    main()
