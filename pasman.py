import os
import json
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, key_file='key.key', data_file='passwords.json'):
        self.key_file = key_file
        self.data_file = data_file
        self.key = self.load_key()
        self.cipher = Fernet(self.key)

    def load_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
            return key
        else:
            with open(self.key_file, 'rb') as key_file:
                return key_file.read()

    def save_password(self, service, username, password):
        encrypted_password = self.cipher.encrypt(password.encode()).decode()
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        
        if service not in data:
            data[service] = []

        data[service].append({
            'username': username,
            'password': encrypted_password
        })

        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_password(self, service, username):
        if not os.path.exists(self.data_file):
            return None
        
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        
        if service in data:
            for account in data[service]:
                if account['username'] == username:
                    encrypted_password = account['password']
                    return self.cipher.decrypt(encrypted_password.encode()).decode()
        return None

    def delete_password(self, service, username):
        if not os.path.exists(self.data_file):
            return
        
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        
        if service in data:
            data[service] = [acc for acc in data[service] if acc['username'] != username]
            if not data[service]:
                del data[service]
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)

def main():
    manager = PasswordManager()

    while True:
        print("\nPassword Manager")
        print("1. Add a new password")
        print("2. Get a password")
        print("3. Delete a password")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            service = input("Enter the service: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            manager.save_password(service, username, password)
            print("Password saved!")
        
        elif choice == '2':
            service = input("Enter the service: ")
            username = input("Enter the username: ")
            password = manager.get_password(service, username)
            if password:
                print(f"Password for {username} on {service}: {password}")
            else:
                print("No password found.")
        
        elif choice == '3':
            service = input("Enter the service: ")
            username = input("Enter the username: ")
            manager.delete_password(service, username)
            print("Password deleted if it existed.")
        
        elif choice == '4':
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
