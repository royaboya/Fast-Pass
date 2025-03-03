import os
from getpass import getpass

class CommandLineView:
    
    def display_splash_text(self):
        splash = """
                                           __                
  ____   ____   ___________ ___.__._______/  |_  ___________ 
_/ __ \ /    \_/ ___\_  __ <   |  |\____ \   __\/  _ \_  __ \\
\  ___/|   |  \  \___|  | \/\___  ||  |_> >  | (  <_> )  | \/
 \___  >___|  /\___  >__|   / ____||   __/|__|  \____/|__|   
     \/     \/     \/       \/     |__|                      
        
        """
        
        print(splash)
      
    def display_options(self):
        print(f"1. add username/password")
        print(f"2. edit username/password [INCOMPLETE]") # have backups?
        print(f"3. show username/password [INCOMPLETE]")
        print(f"4. show usernames [INCOMPLETE]")   
        print(f"5. [?]")
        print(f"6. [?]")
         
    
    def handle_new_user_entry(self):
        username = input("Enter Username: ")
        password = getpass("Enter Password: ")
        verify = getpass("Verify Password: ")    
        
        return username, password, verify
    
    def request_verify_password(self):
        v = getpass("verify password")
        pass
    
    def display_pass(self, password):
        print(f"{0}")
    
    def clear_screen(self):
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
    
    def display_all_passwords(self, passes:str):
        pass
    