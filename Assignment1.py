import os
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

is_on = True

#Main program loop
while is_on:
    print("1.Register 2.Store 3.Read 4.Tamper 5.DeleteUser 6.Exit")
    choice = int(input("choice:"))

    # --- Option 1: Register a new user ---
    if choice == 1:
        username = input("username:")
        password = input("password:")
        HashMode = input("Hash Mode(MD5 or SHA256):")

        # Generate a random 16-byte salt for this user
        Salt = os.urandom(16)
        SaltR =base64.b64encode(Salt).decode()

        print("[debug info]:")
        print(f"generateSalt: {SaltR}")
        print("User registered.")

        # Load existing data or start with empty dictionary
        if os.path.exists("vault.json"):
            with open("vault.json", "r") as f:
                data = json.load(f)
        else:
            data = {}

        # Save user info (salt and hash mode) to vault
        data[username] = {
            "salt": SaltR,
            "hash": HashMode
        }
        with open("vault.json", "w") as f:
            json.dump(data, f)

    # --- Option 2: Store an encrypted note ---
    elif choice == 2:
        usernameC = input("username:")
        passC = input("password:")
        note = input("note:")

        # Load user data and retrieve salt and hash mode
        with open("vault.json", "r") as f:
            data = json.load(f)
            saltC = base64.b64decode(data[usernameC]["salt"])
            hashC = data[usernameC]["hash"]

        # Derive a 32-byte encryption key from salt + password
        combined = saltC + passC.encode()

        if hashC == "SHA256":
            key = hashlib.sha256(combined).digest()
        else:
            part1 = hashlib.md5(combined).digest()
            part2 = hashlib.md5(combined+part1).digest()
            key = part1 + part2

        # Generate random 16-byte IV for AES encryption
        IV = os.urandom(16)

        # Encrypt the note using AES-256 in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, IV)
        cipherText = cipher.encrypt(pad(note.encode(), AES.block_size))

        # Compute integrity hash to detect tampering later
        integrity = hashlib.sha256(IV + cipherText).hexdigest()

        # Convert IV and ciphertext to base64 strings for JSON storage
        iv_str = base64.b64encode(IV).decode()
        cipherText2 = base64.b64encode(cipherText).decode()

        # Save encrypted note data to vault
        data[usernameC]["iv"] = iv_str
        data[usernameC]["cipher"] = cipherText2
        data[usernameC]["integrity"] = integrity
        with open("vault.json", "w") as f:
            json.dump(data, f)

        print("[debug info]:")
        print(f"derived key (first 16 bytes): {key[:16].hex()}")
        print(f"IV: {iv_str}")
        print(f"ciphertext: {cipherText2}")
        print("Encrypted and Stored")



    elif choice == 3:
        username = input("username:")
        password = input("password:")

        with open("vault.json", "r") as f:
            data = json.load(f)
            salt = base64.b64decode(data[username]["salt"])
            iv = base64.b64decode(data[username]["iv"])
            cipher = base64.b64decode(data[username]["cipher"])
            hashmode = data[username]["hash"]
            integrity = data[username]["integrity"]

        combined = salt + password.encode()

        if hashmode == "SHA256":
            key = hashlib.sha256(combined).digest()
        else:
            part1 = hashlib.md5(combined).digest()
            part2 = hashlib.md5(combined + part1).digest()
            key = part1 + part2

        integrity2 = hashlib.sha256(iv + cipher).hexdigest()

        if integrity != integrity2:
            print("Tampering detected")
        else:
            decipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(decipher.decrypt(cipher), AES.block_size).decode()
            print(f"decrypted: {plaintext}")


    elif choice == 4:
        pass

    elif choice == 5:
        pass

    else:
        is_on = False
