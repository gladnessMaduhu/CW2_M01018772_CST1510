import bcrypt
import os
#coorect path to DAT/users.txt
# auth.py is located at: app/data/auth.py
# users.txt must be in:  DATA/users.txt
# So we go two levels up from this file, then into DATA.
USER_DATA_FILE = os.path.join(
    os.path.dirname(__file__),  # app/data/
    "..",                       # app/
    "..",                       # project root/
    "DATA",                     # DATA/
    "users.txt"                 # users.txt
)

# Convert the path to an absolute path
USER_DATA_FILE = os.path.abspath(USER_DATA_FILE)

# Debug print – verify correct file path
print(f"[DEBUG] User data file path: {USER_DATA_FILE}")


#password hashing and verifying
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

#creates DATA/users.txt if it does not exist
def ensure_file_exists():
    directory = os.path.dirname(USER_DATA_FILE)
    os.makedirs(directory, exist_ok=True)
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            pass


def user_exists(username):
    ensure_file_exists()

    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "," not in line:
                continue

            stored_user, _ = line.split(",", 1)
            if stored_user == username:
                return True
    return False


def register_user(username, password):
    ensure_file_exists()

    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed_password = hash_password(password)

    with open(USER_DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{hashed_password}\n")
        f.flush()  # Forces write

    print(f"User '{username}' registered successfully.")
    return True


def login_user(username, password):
    ensure_file_exists()

    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "," not in line:
                continue

            stored_user, stored_hash = line.split(",", 1)

            if stored_user == username:
                return verify_password(password, stored_hash)

    return False

#username validation
def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 20:
        return False, "Username must be no more than 20 characters long."
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    if user_exists(username):
        return False, "Username already exists."
    return True, ""

#password validation
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit."
    return True, ""



USER_DATA_FILE = "../../DATA/users.txt"


# registers a new user and writes it to file
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed_password = hash_password(password)

    # Ensure directory exists
    os.makedirs(os.path.dirname(USER_DATA_FILE) or ".", exist_ok=True)

    with open(USER_DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{hashed_password}\n")
        f.flush()  # Extra safety

    print(f"Username '{username}' registered successfully!")
    return True


def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "," not in line:
                continue
            stored_username, _ = line.split(",", 1)
            if stored_username == username:
                return True
    return False


def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "," not in line:
                continue

            stored_user, stored_hash = line.split(",", 1)
            if stored_user == username:
                return verify_password(password, stored_hash)

    print("Error: Username not found.")
    return False


def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(username) > 20:
        return False, "Username must be no more than 20 characters."
    if not username.isalnum():
        return False, "Username must contain only letters & numbers."
    if user_exists(username):
        return False, "Username already exists."
    return True, ""


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least 1 uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least 1 lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least 1 number."
    return True, ""

# menu showcase
def display_menu():
    print("\n" + "*" * 50)
    print(" Multi-Domain Intelligence Platform ")
    print(" Secure Authentication System ")
    print("*" * 50)
    print("\n[1] Register a new user")
    print("[2] Login user")
    print("[3] Exit")
    print("*" * 50)


def main():
    print("Welcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == "1":
            print("\n--- User Registration ---")
            username = input("Enter username: ").strip()
            valid, msg = validate_username(username)
            if not valid:
                print("Error:", msg)
                continue

            password = input("Enter password: ").strip()
            valid, msg = validate_password(password)
            if not valid:
                print("Error:", msg)
                continue

            if input("Confirm password: ").strip() != password:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == "2":
            print("\n*** User Login ***")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            if login_user(username, password):
                print("\nLogin successful!")
                input("Press Enter to continue...")
            else:
                print("\nLogin failed. Wrong username or password.")

        elif choice == "3":
            print("\nGoodbye!")
            break

        else:
            print("\nError: Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
