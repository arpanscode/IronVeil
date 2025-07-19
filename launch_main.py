
import sys
import parsefile as p
import tkgui as tk
import encryptionEngine as e

if len(sys.argv) < 2: #the program is run without a file path.
    tk.open_settings()

path = sys.argv[1]
p.validate_path(path)

dir_path, name, ext = p.get_metadata(path)
if ext != '.lck': # encrypt the file
    payload = p.read_file(path)
    ext_bin = bytes(ext,'UTF-8')
    out_payload = ext_bin + payload #this will be encrypted and written out.
    out_path = path[:-4] + '.lck' # the file will stay here.
    pwd = e.validate_password()
    out_payload = e.encrypt_file(pwd, out_payload)
    p.replace_file(path, out_path, out_payload) #write the encrypted file
    tk.show_message('S', 'Encryption Successful!')

else: # decrypt the file
    salt, nonce, ciphertext, tag = p.read_encrypted_file(path)
    pwd = e.validate_password()
    out_ext, out_payload = e.decrypt_file(pwd, salt, nonce, ciphertext, tag)
    out_path = path[:-4] + out_ext # the file will stay here.
    p.replace_file(path, out_path, out_payload)#write the decrypted file
    tk.show_message('S', 'Decryption Successful!')