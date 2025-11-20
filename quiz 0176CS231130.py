import random
import datetime
import os
def load_questions(filename):
    questions = {"DSA": [], "DBMS": [], "PYTHON": []}
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 7:
                    category, question, op1, op2, op3, op4, correct = parts
                    data = {
                        "question": question,
                        "options": [op1, op2, op3, op4],
                        "correct": correct.lower()
                    }
                    if category.upper() in questions:
                        questions[category.upper()].append(data)
        return questions
    except FileNotFoundError:
        print("Error: 'question.txt' not found in the folder.")
        return None

def attempt_quiz(category, questions, username):
    category = category.upper()
    if category not in questions or len(questions[category]) == 0:
        print(f"No questions found for {category}.")
        return

    print(f"\n--- {category} QUIZ STARTED ---\n")
    selected = random.sample(questions[category], k=min(5, len(questions[category])))
    score = 0
    total = len(selected)

    for i, q in enumerate(selected, start=1):
        print(f"Q{i}. {q['question']}")
        for idx, option in enumerate(q["options"], start=97):
            print(f"   {chr(idx)}. {option}")
        user_ans = input("Your answer (a/b/c/d): ").strip().lower()

        if user_ans == q["correct"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect! Correct answer: {q['correct']}\n")

    print("Quiz completed!")
    print(f"Final Score: {score}/{total}")

    try:
        with open("scores.txt", "a") as score_file:
            score_line = f"{username}|{category}|{score}/{total}|{datetime.datetime.now()}\n"
            score_file.write(score_line)
            print(f"Score saved for {username}.")
    except Exception as e:
        print(f"Error saving score: {e}")

def register_user():
    print("\n=== STUDENT REGISTRATION ===")
    name = input("Enter full name: ")
    enrollment = input("Enter enrollment number: ")
    branch = input("Enter branch: ")
    year = input("Enter year: ")
    email = input("Enter email: ")
    contact = input("Enter contact number: ")
    address = input("Enter address: ")
    dob = input("Enter date of birth: ")
    username = input("Create username: ")
    password = input("Create password: ")

    if not os.path.exists("students.txt"):
        with open("students.txt", "w") as f:
            f.write("")

    with open("students.txt", "r") as file:
        for line in file:
            existing_username = line.strip().split("|")[0]
            if existing_username == username:
                print("User already exists. Please login.")
                return

    with open("students.txt", "a") as file:
        file.write(f"{username}|{password}|{name}|{enrollment}|{branch}|{year}|{email}|{contact}|{address}|{dob}\n")

    print("Registration successful. Please login to continue.")

def user_login():
    print("\n=== LOGIN ===")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    try:
        with open("students.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")
                if data[0] == username and data[1] == password:
                    print(f"\nWelcome, {data[2]}!")
                    return username
        print("Invalid username or password.")
        return None
    except FileNotFoundError:
        print("No users registered yet. Please register first.")
        return None

def quiz_menu(questions, username):
    while True:
        print("\n=== QUIZ MENU ===")
        print("1. Attempt Quiz")
        print("2. Logout")

        choice = input("Enter choice (1-2): ").strip()
        if choice == "1":
            category = input("Enter category (DSA / DBMS / PYTHON): ").strip().upper()
            if category in ["DSA", "DBMS", "PYTHON"]:
                attempt_quiz(category, questions, username)
            else:
                print("Invalid category. Try again.")
        elif choice == "2":
            print(f"Logged out successfully, {username}.")
            break
        else:
            print("Invalid choice. Try again.")

def main():
    print("=== Welcome to the Student Quiz System ===")
    questions = load_questions("question.txt")
    if not questions:
        return

    while True:
        print("\n=== MAIN MENU ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            register_user()
        elif choice == "2":
            username = user_login()
            if username:
                quiz_menu(questions, username)
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()