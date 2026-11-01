

import csv
from connect import connect


# 1. Show all contacts
def show_contacts():
    connection = connect()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM contacts ORDER BY id")
        contacts = cursor.fetchall()

        if not contacts:
            print("\nPhoneBook is empty.")
        else:
            print("\n========== CONTACTS ==========")
            for contact in contacts:
                print(f"ID: {contact[0]}")
                print(f"Name: {contact[1]}")
                print(f"Phone: {contact[2]}")
                print("------------------------------")

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


# 2. Add a new contact
def add_contact():
    first_name = input("Enter contact name: ").strip()
    phone = input("Enter phone number: ").strip()

    if not first_name or not phone:
        print("Name and phone cannot be empty.")
        return

    connection = connect()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
            (first_name, phone)
        )
        connection.commit()
        print("\nContact added successfully!")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


# 3. Import contacts from CSV
def import_csv():
    connection = connect()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        with open(
            "Practice7/contacts.csv",
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)
            count = 0

            for row in reader:
                first_name = row["first_name"].strip()
                phone = row["phone"].strip()

                if first_name and phone:
                    cursor.execute(
                        """
                        INSERT INTO contacts (first_name, phone)
                        VALUES (%s, %s)
                        """,
                        (first_name, phone)
                    )
                    count += 1

        connection.commit()
        print(f"\nSuccessfully imported {count} contacts!")

    except Exception as error:
        connection.rollback()
        print("Import error:", error)

    finally:
        cursor.close()
        connection.close()


# 4. Search contacts by name or phone prefix
def search_contacts():
    search_value = input("Enter name or phone prefix: ").strip()

    if not search_value:
        print("Search value cannot be empty.")
        return

    connection = connect()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT * FROM contacts
            WHERE first_name ILIKE %s OR phone LIKE %s
            ORDER BY id
            """,
            (f"%{search_value}%", f"{search_value}%")
        )

        contacts = cursor.fetchall()

        if not contacts:
            print("\nNo contacts found.")
        else:
            print("\n========== SEARCH RESULTS ==========")
            for contact in contacts:
                print(
                    f"ID: {contact[0]} | "
                    f"Name: {contact[1]} | "
                    f"Phone: {contact[2]}"
                )

    except Exception as error:
        print("Search error:", error)

    finally:
        cursor.close()
        connection.close()


# 5. Update a contact
def update_contact():
    contact_id = input("Enter the ID of the contact to update: ").strip()

    if not contact_id.isdigit():
        print("Please enter a valid ID.")
        return

    print("\nWhat do you want to update?")
    print("1. First name")
    print("2. Phone number")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        new_value = input("Enter new name: ").strip()
        column = "first_name"
    elif choice == "2":
        new_value = input("Enter new phone number: ").strip()
        column = "phone"
    else:
        print("Invalid option.")
        return

    if not new_value:
        print("New value cannot be empty.")
        return

    connection = connect()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        if column == "first_name":
            cursor.execute(
                "UPDATE contacts SET first_name = %s WHERE id = %s",
                (new_value, int(contact_id))
            )
        else:
            cursor.execute(
                "UPDATE contacts SET phone = %s WHERE id = %s",
                (new_value, int(contact_id))
            )

        if cursor.rowcount == 0:
            print("\nContact with this ID was not found.")
        else:
            connection.commit()
            print("\nContact updated successfully!")

    except Exception as error:
        connection.rollback()
        print("Update error:", error)

    finally:
        cursor.close()
        connection.close()


# 6. Delete a contact by name or phone number
def delete_contact():
    print("\nDelete contact by:")
    print("1. Name")
    print("2. Phone number")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        value = input("Enter contact name: ").strip()
        column = "first_name"
    elif choice == "2":
        value = input("Enter phone number: ").strip()
        column = "phone"
    else:
        print("Invalid option.")
        return

    if not value:
        print("Value cannot be empty.")
        return

    connection = connect()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        if column == "first_name":
            cursor.execute(
                "DELETE FROM contacts WHERE first_name = %s",
                (value,)
            )
        else:
            cursor.execute(
                "DELETE FROM contacts WHERE phone = %s",
                (value,)
            )

        deleted_count = cursor.rowcount
        connection.commit()

        if deleted_count == 0:
            print("\nNo matching contact found.")
        else:
            print(f"\nDeleted {deleted_count} contact(s) successfully!")

    except Exception as error:
        connection.rollback()
        print("Delete error:", error)

    finally:
        cursor.close()
        connection.close()


# 7. Main menu
def main():
    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Show all contacts")
        print("2. Add contact")
        print("3. Import contacts from CSV")
        print("4. Search contacts")
        print("5. Update contact")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            show_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            import_csv()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            update_contact()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
