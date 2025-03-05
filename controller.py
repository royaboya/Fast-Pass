from getpass import getpass

#TODO: encapsulate whole program in a q quit loop or something

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

            while password != v:
                self.view.display_verify_password_entry()
                v = self.view.request_verify_password()
            
            encrypted = self.model.encrypt(password)
            self.model.add_entry_into_mysql(username, encrypted)
            
        elif menu_prompt == "2":
            username = self.view.request_enter_username()
            usernames = self.model.get_all_usernames()
            exists = username in usernames
            
            if exists:
                ciphertext = self.model.get_encrypted_password(username)
                extracted_ciphertext = self.model.extract_sql_fetches(ciphertext, 'password_hash')[0]
                
                plaintext = self.model.decrypt(extracted_ciphertext)
                
                self.view.display_password(username, plaintext)
                

            else:
                print("username does not exist")
            
        elif menu_prompt == "3":
            usernames = self.model.get_all_usernames()
            self.view.display_all_users(usernames)
            
        elif menu_prompt == "4":
            user = self.view.request_enter_username() #TODO: add username checks
            flag = self.view.display_change_user_or_pass() # this should be bool, true -> false == user, pass == true?

            if flag:
                new_user = self.view.request_new_username(user)
                self.model.change_username(user, new_user)
            else:
                #TODO: add another layer of confirmation here
                new_password = self.view.request_new_password()
                verify = self.view.request_verify_password()
                
                while (new_password != verify):
                    verify = self.view.display_verify_password_entry()
                
                new = self.model.encrypt(new_password)
                self.model.change_user_password(user, new)
                self.view.display_success_password_change()
        
        elif menu_prompt == "5":
            user = self.view.request_enter_username()
            # TODO: add verify (thru master password or acc pw?)
            self.model.delete_entry(user)
        
    def clear_logs(self) -> None:
        self.model.clear_model_logs()
        self.view.display_clear_logs()
    
    def request_master_password(self):
        master = self.view.display_request_master()
        
        r = self.model.verify_master_password(master)
        
        #TODO: exit after 3 tries [?]
        while not(r):
            self.view.display_incorrect_password()
            master = self.view.display_request_master()
            r = self.model.verify_master_password(master)
            
        
    
    
    
    