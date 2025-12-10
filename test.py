from data_handler import fetch_user, save_users, save_score, result
# Step 1: Load existing users (or empty if file doesn't exist)
users = fetch_user()
print("Users loaded:", users)

# Step 2: Add a new test user
users["1003"] = {
    "name": "cati",
    "email": "test@example.com",
    "branch": "CSE",
    "year": "3",
    "contact": "1234567890",
    "password": "pass23"
}

# Step 3: Save users back to file
save_users(users)
print("User saved successfully!")
