from cryptography.fernet import Fernet
import logging
import bcrypt
import mysql.connector
import dotenv
import os
from dotenv import dotenv_values, set_key


class EncryptModel:

    def __init__(self):
        self.master_password = None
        self.master_salt = ""
        
        # for now while i figure out how to store keys
        self.k = b"BA760m46kKb_CLJDPsjM3ItdAdUGXw9rf6Nvn9AZiOA="
        self.cipher_suite = Fernet(self.k)
        
        
        self.load_master_password_and_salt()
        
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kali"
        ) 
        self.cursor = self.connection.cursor(dictionary=True)
        
        logging.basicConfig(
            filename="./logs/model_events.log",
            level = logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
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
        
    def add_entry_into_mysql(self, username, password):
        QUERY = "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s)"
        
        """
        the table users:
        mysql> CREATE TABLE users (
            ->     id INT AUTO_INCREMENT PRIMARY KEY,
            ->     username VARCHAR(255) UNIQUE NOT NULL,
            ->     password_hash VARCHAR(255) NOT NULL,                                                                             
            ->     salt VARCHAR(255) NOT NULL,                                                                                      
            ->     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            -> );
        """
        self.cursor.execute("USE development;")
        self.cursor.execute(QUERY, (username, password, "NO SALT"))
        self.connection.commit()
        logging.info(f"Logged entry: {username}")

    def hash_master_password(self, password:str, salt):
        pass_bytes = password.encode()
      
        hash = bcrypt.hashpw(pass_bytes, salt)
        
        return hash.decode('utf-8')
    
    def master_password_exists(self) -> bool:
        return self.master_password != None
    
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
            set_key(env_path, SALT_KEY, self.master_salt)
        else:
            with open(env_path, "a") as env_file:
                env_file.write(f"\n{MASTER_KEY}={hashed}") 
                env_file.write(f"\n{SALT_KEY}={MASTER_SALT.decode()}")
                
        logging.info("Created new master password and salt")
        
    def load_key(self):
        pass
    
if __name__ == "__main__":
    model = EncryptModel()
    assert(model.decrypt(model.encrypt("test")) == "test")
    
    