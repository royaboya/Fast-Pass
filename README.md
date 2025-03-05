## Simple Command Line Password Manager Program

Educational Purposes Only, this is not a truly secure way to store passwords and is only meant for learning

The goal for this short project was to figure out how to work with MYSQL and very general hashing and encryption schemas, and also to
figure out how MVC design worked since I haven't touched upon that in a while.

---
Usage `python main.py`

Expects an `.env` file in the same directory as `main.py`


### TODO (when i have time)
Points of improvement from highest priority to lowest priority (there's a lot.):
- derive the key from the master password instead of hardcoding it since idk what to do with the key rn
- insert master password into the sql database so that users cant just delete the .env file and replace it with their own to get access to the passwords 
- adding onto the previous point then i would need to figure out points of recovery
- input validation (for SQL injection)
- output sanitization (for bad outputs incase of injection or unknown behavior)
- fix the program flow so it doesn't need to be rerun everytime 
- rerequest master password for every decryption action
- making the display temporary for the plaintext passwords so theyre not left in the history
- store more metadata in the SQL table (e.g purpose/website)
- check for nonexistent/duplicate name entries
- use `tabulate` to better display data in the view
- abstract functions to get rid of repetitive code

Libraries used:
```
bcrypt
cryptography
dotenv
getpass
logging
mysql
```
