from data_handler import fetch_user , save_users
from quiz_module import user_panel , admin_panel
def register(users):
    print("---Registration---")
    enroll=(input("enter the enrollment:"))
    if enroll in users:
        print("user already registered. Try login!")
        return users
    name=input("enter the name:")
    email=input("enter the email:")
    branch=input("enter the branch:")
    year=input("enter the year:")
    contact=int(input("enter the contact details:"))
    password=input("enter the password:")
    users[enroll]={
        'name':name,
        'email':email,
        'branch':branch,
        'year':year,
        'contact':contact,
        'password':password,
        
    }
    save_users(users)
    print("user saved successfully!")
    return users 
from quiz_module import user_panel, admin_panel

def login(users):
    print("---login---")
    enroll = input("enter the enrollment:")
    password = input("enter the password:")

    # admin login
    if enroll == "creator299" and password == "no_body@123":
        print("admin logged in successfully!")
        admin_panel()
        return users

    # normal student login
    if enroll in users and users[enroll]["password"] == password:
        print(f"Welcome, {users[enroll]['name']}!")
        user_panel(enroll, users)   # ✅ pass users here
    else:
        print("invalid credentials!")

    return users

        
    
    