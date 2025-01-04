import cryptography
from cryptography.fernet import Fernet

import controller
import encrypt_model
import command_line_view


# import dotenv -> use this to deal with saving keys n shit
# https://stackoverflow.com/questions/63484742/how-to-write-in-env-file-from-python-code

if __name__ == "__main__":
    
    # k = Fernet.generate_key()

    k = b"BA760m46kKb_CLJDPsjM3ItdAdUGXw9rf6Nvn9AZiOA="

    c_suite = Fernet(k)

    i = input("plaintext: ")

    print(c_suite.encrypt(i.encode()))
