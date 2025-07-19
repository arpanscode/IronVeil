import re
import secrets
import sys

import tkgui as tk
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def validate_password() -> str:
    """
    **Validates password against below rule.**\n
    - Must be more than 8 characters long.\n
    - Must have at last one upper case.\n
    - Must have at last one lower case.\n
    - Must have at last one number.\n
    - Must have at last one special character.
    - Allowed special characters: @_!#$%^&*()<>?/|{}~:

    :return: password: the password String (unencrypted)
    """
    while True:
        password = tk.getpass()

        special_chr = re.compile('[@_!#$%^&*()<>?/|}{~:]')
        var_ok = False
        if password is None:
            sys.exit(1)

        if len(password) > 8:
            if re.search('[a-z]',password):
                if re.search('[A-Z]', password):
                    if re.search('[0-9]', password):
                        if re.search(special_chr,password):
                            var_ok = True
        if var_ok:
            break
        else:
            tk.show_message('S',
                            """Please Specify password as below: \n\n
                                - Must be more than 8 characters long.\n
                                - Must have at last one upper case.\n
                                - Must have at last one lower case.\n
                                - Must have at last one number.\n
                                - Must have at last one special character.\n\n
                                - Allowed special characters:\n @_!#$%^&*()<>?/|{}~:
                            """
                            )
    return password

def get_salt() -> bytes:
    """
    Get 32 byte salt
    """
    return secrets.token_bytes()

def get_nonce() -> bytes:
    """
    get 16 byte nonce
    """
    return secrets.token_bytes(16)

def get_hashed_key(password: str,salt: bytes) -> bytes:
    """
    get SHA-256 hashed key from Password and salt.
    :param password: unencrypted password text
    :param salt: salt bytes
    :return:  of hash key for encryption
    """
    return PBKDF2(password=password,salt=salt, dkLen=32, count=200000, hmac_hash_module=SHA256)

def get_secure_encrypted(payload: bytes, key: bytes, nonce: bytes) -> tuple[bytes, bytes]:
    """
    encrypt data using AES-GCM
    :param payload: bytes to be encrypted { original file + extension }
    :param key: hashed key for encryption { SHA-256 }
    :param nonce: nonce { 16 bytes }
    :return: ciphertext, tag
    """
    cipher = AES.new(key=key,mode=AES.MODE_GCM,nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(payload)
    return ciphertext, tag

def get_secure_decrypted(payload: bytes, key: bytes, nonce: bytes, tag: bytes) -> bytes:
    """
    decrypt the LCK file into plaintext
    :param payload: bytes of the ciphertext
    :param key: bytes of the decryption key
    :param nonce: bytes of nonce
    :param tag: bytes of validation tag
    :return: bytes of plaintext
    """
    try:
        cipher = AES.new(key=key,mode=AES.MODE_GCM,nonce=nonce)
        plaintext = cipher.decrypt_and_verify(payload,tag)
        return plaintext
    except ValueError:
        tk.show_message('E', 'Invalid Password')
        sys.exit(1)

def encrypt_file(password: str, payload: bytes) -> bytes:
    """
    encrypt file using password
    :param password:  unencrypted string
    :param payload: bytes of plaintext
    :return: bytes of lck file
    """
    salt = get_salt()
    key = get_hashed_key(password,salt)
    nonce = get_nonce()
    ciphertext, tag = get_secure_encrypted(payload, key, nonce)
    out_load = salt + nonce + ciphertext + tag
    return out_load

def decrypt_file(password: str, salt: bytes, nonce: bytes, ciphertext: bytes, tag: bytes) -> tuple[str, bytes]:
    """
    decrypt the lck file into the plaintext file
    :param password: unencrypted password
    :param salt: salt bytes
    :param nonce: nonce bytes
    :param ciphertext: cipher text bytes
    :param tag: validation tag bytes
    :return: extension of the original file, bytes of the original file
    """
    key = get_hashed_key(password,salt)
    plaintext = get_secure_decrypted(ciphertext,key,nonce,tag)
    out_ext = plaintext[:4].decode('UTF-8') #[bytes: 0 to 3] UP-TO but NOT including 4
    out_payload = plaintext[4:]
    return out_ext, out_payload







