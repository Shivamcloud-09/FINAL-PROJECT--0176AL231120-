from data_handler import fetch_user
from register_login import register,login 
def main():
    users=fetch_user()
    while True:
        print("-----WELCOME-----")
        print("1.Register")
        print("2.Login")
        print("3.Exit")
        get_choice=int(input("enter the choice:"))
        if get_choice==1:
            users=register(users)
            continue
        if get_choice==2:
            users=login(users)
            return
        if get_choice==3:
            print("Thank You Exiting")
            continue
        else:
            print("invalid choice")
if __name__=="__main__":
    main()
            