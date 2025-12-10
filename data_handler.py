from firebase_config import db
import datetime

# -------------------------------
# FETCH all users from Firebase
# -------------------------------
def fetch_user():
    users = {}
    docs = db.collection("students").get()

    for doc in docs:
        data = doc.to_dict()
        enroll = data.get("enroll")

        users[enroll] = {
            "name": data.get("name"),
            "email": data.get("email"),
            "branch": data.get("branch"),
            "year": data.get("year"),
            "contact": data.get("contact"),
            "password": data.get("password"),
        }
    return users


# -------------------------------
# SAVE users to Firebase
# -------------------------------
def save_users(users):
    for enroll, info in users.items():
        db.collection("students").document(enroll).set({
            "enroll": enroll,
            "name": info["name"],
            "email": info["email"],
            "branch": info["branch"],
            "year": info["year"],
            "contact": info["contact"],
            "password": info["password"],
        })


# -------------------------------
# SAVE score to Firebase
# -------------------------------
def save_score(enroll, category, score, total):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.collection("quiz_scores").add({
        "enroll": enroll,
        "category": category,
        "score": f"{score}/{total}",
        "date": now
    })


# -------------------------------
# FETCH quiz results (for admin)
# -------------------------------
def result():
    docs = db.collection("quiz_scores").get()

    records = []
    for doc in docs:
        records.append(doc.to_dict())

    return records
