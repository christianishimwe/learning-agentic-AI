import unittest
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import add_contact, list_contacts, search_contact, CONTACTS_FILE, _save_contacts

class TestContactBook(unittest.TestCase):

    def setUp(self):
        # Ensure a clean contacts file before each test
        if os.path.exists(CONTACTS_FILE):
            os.remove(CONTACTS_FILE)
        _save_contacts({})

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(CONTACTS_FILE):
            os.remove(CONTACTS_FILE)

    def test_add_contact(self):
        result = add_contact("Alice", "111-222-3333")
        self.assertEqual(result, "Contact 'Alice' added.")
        with open(CONTACTS_FILE, 'r') as f:
            contacts = json.load(f)
        self.assertEqual(contacts, {"Alice": "111-222-3333"})

    def test_add_multiple_contacts(self):
        add_contact("Alice", "111-222-3333")
        add_contact("Bob", "444-555-6666")
        with open(CONTACTS_FILE, 'r') as f:
            contacts = json.load(f)
        self.assertEqual(contacts, {"Alice": "111-222-3333", "Bob": "444-555-6666"})

    def test_list_contacts_empty(self):
        result = list_contacts()
        self.assertEqual(result, "No contacts found.")

    def test_list_contacts_non_empty(self):
        add_contact("Alice", "111-222-3333")
        add_contact("Bob", "444-555-6666")
        result = list_contacts()
        expected_output = "--- Your Contacts ---\nName: Alice, Phone: 111-222-3333\nName: Bob, Phone: 444-555-6666"
        self.assertEqual(result, expected_output)

    def test_search_contact_found(self):
        add_contact("Alice", "111-222-3333")
        result = search_contact("Alice")
        self.assertEqual(result, "Name: Alice, Phone: 111-222-3333")

    def test_search_contact_not_found(self):
        add_contact("Alice", "111-222-3333")
        result = search_contact("Charlie")
        self.assertEqual(result, "Contact 'Charlie' not found.")

    def test_add_contact_overwrite(self):
        add_contact("Alice", "111-222-3333")
        add_contact("Alice", "999-888-7777") # Overwrite
        with open(CONTACTS_FILE, 'r') as f:
            contacts = json.load(f)
        self.assertEqual(contacts, {"Alice": "999-888-7777"})

if __name__ == '__main__':
    unittest.main()
