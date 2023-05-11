from cryptography.fernet import Fernet

def new_key(key_file):
    key = Fernet.generate_key()
    file = open(key_file, "wb")
    file.write(key)
    file.close()

def load_key(key_file):
    file = open(key_file, "rb")
    return file.read()

def encrypt_message(message, key_file):
    key = load_key(key_file)
    f = Fernet(key)
    return f.encrypt(message)

def encrypt(filename, key_file):
    file = open(filename, "rb")
    message = file.read()
    file.close()
    encrypted = encrypt_message(message, key_file)
    file = open(filename, "wb")
    file.write(encrypted)
    file.close()
    #messagebox.showinfo("this is a window", "this is a message, your file was encrypted")

def decrypt_message(message, key_file):
    key = load_key(key_file)
    f = Fernet(key)
    return f.decrypt(message)

def decrypt(filename, key_file):
    file = open(filename, "rb")
    message = file.read()
    file.close()
    decrypted = decrypt_message(message, key_file)
    file = open(filename, "wb")
    file.write(decrypted)
    file.close()