import json
import os

CONTACTS_FILE = 'contacts.json'

def _load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return {}
    with open(CONTACTS_FILE, 'r') as f:
        return json.load(f)

def _save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=4)

def add_contact(name, phone):
    contacts = _load_contacts()
    contacts[name] = phone
    _save_contacts(contacts)
    return f"Contact '{name}' added."

def list_contacts():
    contacts = _load_contacts()
    if not contacts:
        return "No contacts found."
    
    output = ["--- Your Contacts ---"]
    for name, phone in contacts.items():
        output.append(f"Name: {name}, Phone: {phone}")
    return "\n".join(output)

def search_contact(name):
    contacts = _load_contacts()
    phone = contacts.get(name)
    if phone:
        return f"Name: {name}, Phone: {phone}"
    return f"Contact '{name}' not found."

def main():
    while True:
        print("\nContact Book CLI")
        print("1. Add Contact")
        print("2. List Contacts")
        print("3. Search Contact")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter contact name: ")
            phone = input("Enter contact phone number: ")
            print(add_contact(name, phone))
        elif choice == '2':
            print(list_contacts())
        elif choice == '3':
            name = input("Enter contact name to search: ")
            print(search_contact(name))
        elif choice == '4':
            print("Exiting Contact Book. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
