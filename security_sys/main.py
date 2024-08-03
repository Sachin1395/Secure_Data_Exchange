
USERS={
    "admin":"123"
}

class Login():
    def __init__(self):
        self.logged_in = False
        self.username=""

    def login(self):
        print("\t\tWelcome !!\n\n")

        while self.logged_in == False:
            self.user_name = input("Enter yor User Name : ")
            password = input("Enter your password : ")
            for user in USERS:
                if self.user_name not in USERS:
                    print("No user found!\n\n")
                    pass
                if self.user_name in USERS:
                    if self.user_name == user:
                        if password == USERS[user]:
                            print("\nlogin successfull\n")
                            self.logged_in = True
                            return True
                        else:
                            print("wrong password!")






#log in -----------------------------------x





'''
#access api with token
***
access = False
while access==False :
    access_key = input("Enter access key : ")
    if access_key== access_token_gen.password:
        access=True
        print("enter private key password : ")

    else:
        print("Invalid key")
'''







