import os
import os.path as _path
import sys
import tkgui as tk

def read_file(path: str) -> bytes:
    """
    Read files in binary mode
    :param path: full path of the file
    :return: Bytes of the file
    """
    try:
        with open(path, "rb") as myFile:
            bin_dat = myFile.read()
    except FileNotFoundError:
        tk.show_message('E', 'File not found')
        sys.exit(1)
    except IsADirectoryError:
        tk.show_message('E', 'Expected a file, got a Directory')
        sys.exit(1)
    except PermissionError:
        tk.show_message('E', 'Permission Denied')
        sys.exit(1)
    return bin_dat

def write_file(path: str, bin_dat: bytes) -> bool:
    """
    write file in binary mode
    :param path: full output path
    :param bin_dat: bytes of the payload
    :return: Boolean confirming success
    """
    try:
        with open(path, 'wb') as newfile:
            newfile.write(bin_dat)
    except Exception:
        val_ok = False
    else:
        val_ok = True

    return val_ok

def get_metadata(path : str) -> tuple[str, str, str]:
    """
    **get directory path, name and extension of a file**\n
        1. directory path excluding name of the file\n
        2. just the name of the file without the extension\n
        3. extension of the file
    :param path: full path of file
    :return:
    """
    dir_path = _path.dirname(path)
    name = _path.basename(path)
    name, ext = _path.splitext(name)
    return dir_path, name, ext

def delete_file(path: str) -> bool:
    """
    remove file from a specified path
    :param path: full path
    :return: boolean confirming success
    """
    try:
        os.remove(path)
    except Exception:
        val_ok = False
    else:
        val_ok = True

    return val_ok

def read_encrypted_file(path: str) -> tuple[bytes, bytes, bytes, bytes]:
    """
    Read .lck file and break it into components.
    :param path: full path of the .lck file
    :return: salt, nonce, ciphertext, tag
    """
    try:
        with open(path, 'rb') as myFile:
            salt = myFile.read(32)
            nonce = myFile.read(16)
            payload = myFile.read()
            ciphertext = payload[:-16]
            tag = payload[-16:]
        return salt, nonce, ciphertext, tag
    except FileNotFoundError:
        tk.show_message('E', 'File not found')
        sys.exit(1)

def replace_file(path: str, out_path: str, out_payload: bytes) -> None:
    """
    replace old file with new file
    :param path: full path of old file
    :param out_path: full path of new file
    :param out_payload: contents of new file
    :return:
    """
    v_ok = write_file(out_path,out_payload) #write the encrypted file
    if v_ok:
        v_ok = delete_file(path) # delete original
    else:
        tk.show_message('E', 'Cannot replace file')
        sys.exit(1)
    if not v_ok:
        tk.show_message('E', 'Cannot replace file')
        sys.exit(1)

def validate_path(path: str):
    if os.path.isdir(path):
        tk.show_message('E', 'Cannot Encrypt Directories')
        sys.exit(1)

