import logging
import os

import bcrypt
import mysql.connector
import dotenv
from dotenv import dotenv_values, set_key

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


"""
the table users (for testing)
mysql> CREATE TABLE users (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     username VARCHAR(255) UNIQUE NOT NULL,
    ->     password_hash VARCHAR(255) NOT NULL,                                                                             
    ->     salt VARCHAR(255) NOT NULL,                                                                                      
    ->     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -> );
"""

class EncryptModel:


    # require sql credentials on instantiation?
    def __init__(self):
        self.master_password = None
        self.master_salt = ""
        
        # derive key from master password instead of hardcoding 
        # how to store master password???
        self.k = b"BA760m46kKb_CLJDPsjM3ItdAdUGXw9rf6Nvn9AZiOA="
        self.cipher_suite = Fernet(self.k)
        
        self.load_master_password_and_salt()
        
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kali"
        ) 
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute("use development")
        
        logging.basicConfig(
            filename="./logs/model_events.log",
            level = logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        

    def encrypt(self, plaintext:str):
        cs = Fernet(self.k)
        logging.info("String Encryption event") 
        return cs.encrypt(plaintext.encode())        

    def decrypt(self, ciphertext) -> str:
        cs = Fernet(self.k)
        logging.info("String Decryption Event")
        return cs.decrypt(ciphertext).decode()
    
    def key_exists(self) -> bool:
        return self.k != None
    
    def clear_model_logs(self):
        try:
            with open("./logs/model_events.log", "w") as log:
                log.truncate(0)
        except:
            print("Unable to find model_events.log")

    def verify_master_password(self, password:str) -> bool:
        hashed = self.hash_master_password(password, self.master_salt)
        
        return hashed == self.master_password
        
    def load_master_password_and_salt(self):
        try:
            dotenv.load_dotenv()
            master = os.getenv("MASTER_HASH")
            salt = os.getenv("MASTER_SALT").encode()
            
            self.master_password = master
            self.master_salt = salt
        except:
            self.master_password = None
            self.master_salt = None
        
        
    # currently does not check for duplicates
    def add_entry_into_mysql(self, username, password):
        QUERY = "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s)"

        self.cursor.execute(QUERY, (username, password, "NO SALT"))
        self.connection.commit()
        logging.info(f"Logged entry: {username}")

    def hash_master_password(self, password:str, salt):
        pass_bytes = password.encode()
      
        hash = bcrypt.hashpw(pass_bytes, salt)
        
        return hash.decode('utf-8')
    
    def master_password_exists(self) -> bool:
        return self.master_password != None and self.master_password != ""
    
    def create_new_master_password(self, new_pass):
        MASTER_KEY = "MASTER_HASH"
        SALT_KEY = "MASTER_SALT"
        
        MASTER_SALT = bcrypt.gensalt()
    
        self.master_password = new_pass
        self.master_salt = MASTER_SALT
        
        env_path = ".env"
        config = dotenv_values(env_path)    
        
        hashed = self.hash_master_password(new_pass, MASTER_SALT)

        if MASTER_KEY and SALT_KEY in config:
            set_key(env_path, MASTER_KEY, hashed)
            set_key(env_path, SALT_KEY, MASTER_SALT.decode())
        else:
            with open(env_path, "a") as env_file:
                env_file.write(f"\n{MASTER_KEY}={hashed}") 
                env_file.write(f"\n{SALT_KEY}={MASTER_SALT.decode()}")
                
        logging.info("Created new master password and salt")
        
        
    def get_all_usernames(self):
        QUERY = "SELECT username FROM users"

        self.cursor.execute(QUERY)
        
        result = self.cursor.fetchall()
        users = [entry["username"] for entry in result]
        
        logging.info(f"Get All Users Called")
        
        return users
        
    def get_encrypted_password(self, username):
        QUERY = "SELECT password_hash FROM users WHERE username = %s"        
        self.cursor.execute(QUERY, (username,))
        
        result = self.cursor.fetchall()
        return result
    
    def user_quit(self, character):
        # todo: check if character is within bounds
        return character == 'q'
        
        
    def load_key(self):
        pass
    
    
    def create_new_key(self):
        # if user already has key, deny or ask for override
        metadata = {
            f"creation time:{''}",
            f"purpose:{''}",
            f"type:{''}", 
        }
        
        logging.info("Key Creation Event")
        
        return Fernet.generate_key()
        
    def remove_key(self):
        logging.info("Key Deletion Event")
        pass
    
    def extract_sql_fetches(self, sql_result, keyname):
        return [entry[keyname] for entry in sql_result]
    
    # holy moly repetitive code need to abstract
    def change_user_password(self, username, password_cipher_text):
        QUERY = "UPDATE USERS SET password_hash = %s WHERE username = %s"
        
        self.cursor.execute(QUERY, (password_cipher_text, username))
        self.connection.commit()
        
    def change_username(self, username, new_username):
        QUERY = "UPDATE USERS SET username = %s WHERE username = %s"
      
        self.cursor.execute(QUERY, (new_username, username))
        self.connection.commit()
    
    def delete_entry(self, username):
        QUERY = "DELETE FROM users WHERE username = %s"
     
        self.cursor.execute(QUERY, (username,))
        self.connection.commit()        
        
    
if __name__ == "__main__":
    model = EncryptModel()
    assert(model.decrypt(model.encrypt("test")) == "test")
    
    