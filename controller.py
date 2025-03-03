from getpass import getpass

#TODO: encapsulate whole program in a q quit loop

class Controller:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def run(self):
        self.view.display_splash_text()
        
        m_exists = self.model.master_password_exists()
        
        if not(m_exists):
            new = self.view.display_create_master()
            self.model.create_new_master_password(new)
        else:
            self.request_master_password()
        
        self.view.display_options()
        
        menu_prompt = str(input(": ")).strip()
        
        if menu_prompt == "1":
            username, password, v = self.view.handle_new_user_entry()

            # move this logic to view
            while password != v:
                print("password is not the same, re-enter password or q to cancel")
                v = getpass("Verify Password: ")
            
            encrypted = self.model.encrypt(password)
            self.model.add_entry_into_mysql(username, encrypted)
            
        elif menu_prompt == "2":
            # rename a username or password
            
            pass
        elif menu_prompt == "3":
            # show usernames
            # self.model.get_list_of_users()
            
            pass
        elif menu_prompt == "4":
            # show a username/password
            # self.model.get_user()
            pass
        
        elif menu_prompt == "5":
            # delete entry
            pass
        
    def clear_logs(self):
        self.model.clear_model_logs()
        self.view.display_clear_logs()
    
    #TODO: move to view
    def request_master_password(self):
        master = self.view.display_request_master()
        
        r = self.model.verify_master_password(master)
        
        # while loop this in view, exit after 3 tries
        while not(r):
            self.view.display_incorrect_password()
            master = self.view.display_request_master()
            r = self.model.verify_master_password(master)
            
    def get_input(self, prompt:str):
        return str(input(prompt)).strip()

        
    
    
    
    