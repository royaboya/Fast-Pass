import os
from getpass import getpass
import sys

class CommandLineView:
    
    def display_splash_text(self) -> None:
        splash = """
                                           __                
  ____   ____   ___________ ___.__._______/  |_  ___________ 
_/ __ \ /    \_/ ___\_  __ <   |  |\____ \   __\/  _ \_  __ \\
\  ___/|   |  \  \___|  | \/\___  ||  |_> >  | (  <_> )  | \/
 \___  >___|  /\___  >__|   / ____||   __/|__|  \____/|__|   
     \/     \/     \/       \/     |__|                      
        
        """
        
        print(splash)
      
    def display_options(self) -> None:
        print(f"1. add username/password")
        print(f"2. get username/password") # have backups?
        print(f"3. show all usernames")
        print(f"4. edit username/password")   
        print(f"5. remove entry")
        print(f"6. [?]")
         
    
    def handle_new_user_entry(self):
        username = input("Enter Username: ")
        password = getpass("Enter Password: ")
        verify = getpass("Verify Password: ")    
        
        return username, password, verify
    
    def request_verify_password(self):
        pw_to_verify = getpass("Verify password: ")
        return pw_to_verify

        
    def request_enter_username(self):
        user = input("Enter the username: ")
        return user
    
    def request_new_username(self, old_username):
        return input(f"Enter a new username for {old_username}: ")
    
    def display_verify_password_entry(self):
        return getpass("password is not the same, re-enter password: ")
    
    def display_username_does_not_exist(self):
        print("Username does not exist!")
    
    def clear_latest_line(self):
        sys.stdout.write("\033[F\033[K")
        sys.stdout.flush()
    
    
    def display_pass(self, password):
        print(f"{0}")
    
    def clear_screen(self) -> None:
        cmd = "cls" if os.name == "nt" else "clear"
        os.system(cmd)
        
    def display_clear_logs(self):
        print("Logs cleared")
        
        
    def display_request_master(self):
        m = getpass("enter master password: ")
        return m
    
    def display_create_master(self):
        new_master = getpass("Create a master password (KEEP IT STRONG)")
        return new_master
    
    def display_incorrect_password(self):
        print("Wrong password, try again.")
        
    def display_all_users(self, username_list):
        PASSWORD_PLACEHOLDER = " | Password: ************"
        
        max_len = max(len(user) for user in username_list)
        max_len_padding = max_len + len(PASSWORD_PLACEHOLDER)
        
        print((max_len_padding + 3) * '=')
        print("=== Users ===".center(max_len_padding + 3))
        print((max_len_padding + 3) * '=')
        
        count = 1
        for user in username_list:
            print(f"{count}. {user.ljust(max_len)}{PASSWORD_PLACEHOLDER}")
            count += 1 
    
    def display_password(self, username, plaintext):
        print(f"Username: {username} | Password: {plaintext}")
        pass
            
    def display_change_user_or_pass(self) -> bool:
        # TODO: assert input is only one character long
        
        PROMPT = "Would you like to change a username or password? (enter u or p): "
        
        choice = " "
        
        while(choice not in 'up'):
            print(choice)
            choice = input(PROMPT)
        
        return choice == "u" 
    
    def request_new_password(self):
        return getpass("Enter a new password: ")
    
    
    def display_success_password_change(self):
        print("Successfully changed passwords")
    