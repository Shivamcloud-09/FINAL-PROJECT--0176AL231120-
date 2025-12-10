from firebase_config import db

def upload_from_txt(category, filename):
    questions = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 6:
                questions.append({
                    "question": parts[0],
                    "options": parts[1:5],
                    "correct": parts[5]
                })
    
    # upload to Firestore
    db.collection("quiz_questions").document(category).set({
        "questions": questions
    })

def upload_questions():
    upload_from_txt("DBMS", "dbms_ques.txt")
    upload_from_txt("DSA", "dsa_ques.txt")
    upload_from_txt("PYTHON", "python_ques.txt")

    print("Questions uploaded successfully from txt files!")

if __name__ == "__main__":
    upload_questions()
