# imports
import json


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


def login():
    # input username and check if it is in the file
    username = input("Enter username: ")
    # open the file and load into a dictionary
    with open("users.json", "r") as f:
        users_data = json.load(f)
    username_list = users_data.keys()
    if username in username_list:
        # if username exists, check password
        password = input("Enter password: ")
        # compare to real password
        real_password = users_data.setdefault(username)
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


def user_options():
    print("If you wish to make changes to a current program enter 0, if you wish to create a new program enter 1: ")
    while True:
        choice = input("Enter your choice: ")
        if choice == 1 or choice == 0:
            break
        print("Invalid choice.")
    if choice == 0:
    # TODO: edit_program()
    else:
    # TODO: create_program()


def main():
    # check if user is new and login or create user accordingly
    user_exists = welcome()
    if user_exists:
        logged_in = login()
        if not logged_in:
            print("You should attempt to login again.")
    else:
        print("We shall start creating your profile!")
        create_user()



if __name__ == '__main__':
    main()
