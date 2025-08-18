**DISCLAIMER: This is just for demonstration and exploration purposes. I don't claim by any means that this is production ready!**

IRON VEIL: Python app to password protect any File
-
This is a basic python code to encrypt any file using a password. 
The code converts your password into a 256 bit key and uses it to encrypt your file data.
Password is not stored. only the salt and nonce is stored, which is used to derive the password.
A tag is stored to check the file's integrity.
Basic TKINTER Dialoguebox is used to get the password and show messages.

INSTRUCTIONS:
-
The app is designed to use by right clicking on a file and then Choosing "Lock with IronVeil".
To do this you need to edit windows registry to:
1. associate the lock file with the app's .exe file.
2. create a context menu to allow "*right click > lock*" option.

Instructions to Edit Regitry:
-
1. Download the reg_edit_add.txt file.
2. Chnage the file paths as per your own file paths.
3. save the file as *IronVeil.reg*.

You can convert the *launch_main.py* file into a *.exe* file using pyinstaller or download the *.exe* file from releases.

FEATURES:
-
- any file type can be encrypted. ( file type is stored as part of the ciphertext ).
- AES-GCM Encryption implementation.
- SHA-256 Hash function.
- Salt and Nonce used to generate encryption/decryption key without saving password.
- TAG is used to check for authentication.
- *OPTIONAL:* Registry can be edited to add *right click > lock / unlock* functionality

screenshots
-
<img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/54156080-1049-454c-9996-9960e15fd9b6" />
<img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/8e66a9a6-7498-412e-8622-6966264e52e3" />
<img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/bbee81ff-5fce-4074-be98-021c02465bbf" />


