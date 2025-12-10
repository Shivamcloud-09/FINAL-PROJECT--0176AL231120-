import random
from firebase_config import db
from data_handler import save_users


# ------------------- LOAD QUESTIONS FROM FIREBASE -------------------
def load_questions():
    categories = {}

    docs = db.collection("quiz_questions").stream()
    for doc in docs:
        # Document ID is the category name: DSA, DBMS, PYTHON
        category = doc.id.upper()
        data = doc.to_dict()

        questions_list = data.get("questions", [])
        categories[category] = []

        for q in questions_list:
            question = q.get("question")
            options = q.get("options", [])
            correct = str(q.get("correct"))

            # basic validation
            if question and len(options) == 4 and correct in {"1", "2", "3", "4"}:
                categories[category].append((question, options, correct))

    return categories


QUIZ_QUESTIONS = load_questions()


# ---------------------- SAVE SCORE TO FIREBASE -----------------------
def save_score_firebase(enroll, category, score, total):
    db.collection("quiz_scores").add({
        "enroll": enroll,
        "category": category,
        "score": score,
        "total": total
    })
    print("Score saved successfully!")


# ----------------------------- QUIZ LOGIC ----------------------------
def quiz_attempt(enroll):
    global QUIZ_QUESTIONS
    QUIZ_QUESTIONS = load_questions()  # reload latest questions

    if not QUIZ_QUESTIONS:
        print("No questions found in database!")
        return

    print("Available Categories:")
    for c in QUIZ_QUESTIONS.keys():
        print("-", c)

    choice = input("Enter quiz category: ").strip().upper()

    if choice not in QUIZ_QUESTIONS:
        print("Invalid category!")
        return

    questions = QUIZ_QUESTIONS[choice]
    random.shuffle(questions)
    score = 0

    for i, (question, options, right) in enumerate(questions, start=1):
        print(f"\nQ{i}. {question}")
        for j, opt in enumerate(options, start=1):
            print(f"  {j}. {opt}")

        ans = input("Enter correct option (1-4): ").strip()

        if ans in {"1", "2", "3", "4"}:
            if ans == right:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! Correct answer was option {right}.")
        else:
            print("Invalid option, question skipped.")

    print(f"\nFinal Score: {score}/{len(questions)}")
    save_score_firebase(enroll, choice, score, len(questions))


# ----------------------------- USER PANEL ----------------------------
def user_panel(enroll, users):
    while True:
        print("\n--- USER PANEL ---")
        print("1. Attempt Quiz")
        print("2. View Profile")
        print("3. Update Profile")
        print("4. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            quiz_attempt(enroll)

        elif choice == "2":
            u = users.get(enroll)
            if not u:
                print("User not found in local data!")
                continue

            print("\nUser Profile:")
            print(f"Name   : {u['name']}")
            print(f"Email  : {u['email']}")
            print(f"Branch : {u['branch']}")
            print(f"Year   : {u['year']}")
            print(f"Contact: {u['contact']}")

        elif choice == "3":
            u = users.get(enroll)
            if not u:
                print("User not found, cannot update.")
                continue

            print("\n--- Update Profile ---")
            u["email"] = input("New Email: ")
            u["contact"] = input("New Contact: ")
            u["branch"] = input("New Branch: ")
            u["year"] = input("New Year: ")

            save_users(users)
            print("Profile updated successfully!")

        elif choice == "4":
            print("Logged out!")
            break

        else:
            print("Invalid choice! Please try again.")


# ----------------------------- ADMIN PANEL ----------------------------
def admin_panel():
    print("\n--- ADMIN PANEL ---")
    print("Quiz Performance Records:\n")

    docs = db.collection("quiz_scores").stream()
    print(f"{'Enrollment':<15}{'Category':<15}{'Score':<10}")
    print("-" * 45)

    found = False
    for doc in docs:
        found = True
        data = doc.to_dict()
        score_text = f"{data.get('score', 0)}/{data.get('total', 0)}"
        print(f"{data.get('enroll', 'N/A'):<15}{data.get('category', 'N/A'):<15}{score_text:<10}")

    if not found:
        print("No quiz records found.")
