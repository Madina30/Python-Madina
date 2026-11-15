
import csv
import json
import os
from datetime import date

from connect import connect


# ==========================================
# 1. DISPLAY CONTACT
# ==========================================

def display_contact(contact):
    print("\n----------------------------------------")
    print(f"ID: {contact[0]}")
    print(f"Name: {contact[1]}")
    print(f"Email: {contact[2] or 'Not specified'}")
    print(f"Birthday: {contact[3] or 'Not specified'}")
    print(f"Group: {contact[4] or 'Not specified'}")
    print(f"Date added: {contact[5] or 'Not specified'}")

    if contact[6]:
        print("Phone numbers:")
        for phone in contact[6]:
            print(f"  - {phone[0]} ({phone[1]})")
    else:
        print("Phone numbers: None")

    print("----------------------------------------")


# ==========================================
# 2. GET CONTACTS
# ==========================================

def get_contacts(query="", params=(), sort_by="name"):
    connection = connect()

    if connection is None:
        return []

    cursor = connection.cursor()

    sort_options = {
        "name": "c.first_name ASC",
        "birthday": "c.birthday ASC NULLS LAST",
        "created_at": "c.created_at ASC"
    }

    order_by = sort_options.get(sort_by, "c.first_name ASC")

    try:
        sql = f"""
            SELECT
                c.id,
                c.first_name,
                c.email,
                c.birthday,
                g.name,
                c.created_at,
                ARRAY(
                    SELECT ARRAY[p.phone, p.type]
                    FROM phones p
                    WHERE p.contact_id = c.id
                    ORDER BY p.id
                )
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            {query}
            ORDER BY {order_by};
        """

        cursor.execute(sql, params)
        return cursor.fetchall()

    except Exception as error:
        print("Database error:", error)
        return []

    finally:
        cursor.close()
        connection.close()


# ==========================================
# 3. SHOW ALL CONTACTS
# ==========================================

def show_contacts():
    contacts = get_contacts()

    if not contacts:
        print("\nPhoneBook is empty.")
        return

    print("\n========== ALL CONTACTS ==========")

    for contact in contacts:
        display_contact(contact)


# ==========================================
# 4. ADD CONTACT
# ==========================================

def add_contact():
    print("\n========== ADD CONTACT ==========")

    name = input("Enter contact name: ").strip()
    phone = input("Enter phone number: ").strip()
    phone_type = input(
        "Enter phone type (home/work/mobile): "
    ).strip().lower()

    email = input("Enter email: ").strip() or None
    birthday = input(
        "Enter birthday (YYYY-MM-DD): "
    ).strip() or None

    group_name = input("Enter group: ").strip()

    if not name or not phone:
        print("Name and phone cannot be empty.")
        return

    if phone_type not in ("home", "work", "mobile"):
        print("Invalid phone type.")
        return

    if birthday:
        try:
            date.fromisoformat(birthday)
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
            return

    connection = connect()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        group_id = None

        if group_name:
            cursor.execute(
                "SELECT id FROM groups WHERE name ILIKE %s LIMIT 1",
                (group_name,)
            )
            result = cursor.fetchone()

            if result is None:
                print("Group not found. Contact not added.")
                return

            group_id = result[0]

        cursor.execute("""
            INSERT INTO contacts
                (first_name, phone, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (name, phone, email, birthday, group_id))

        contact_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s);
        """, (contact_id, phone, phone_type))

        connection.commit()
        print("Contact added successfully!")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


# ==========================================
# 5. FILTER BY GROUP
# ==========================================

def filter_by_group():
    group_name = input("Enter group name: ").strip()

    if not group_name:
        print("Group name cannot be empty.")
        return

    contacts = get_contacts(
        "WHERE g.name ILIKE %s",
        (group_name,)
    )

    if not contacts:
        print("No contacts found in this group.")
        return

    for contact in contacts:
        display_contact(contact)


# ==========================================
# 6. SEARCH BY EMAIL
# ==========================================

def search_by_email():
    email_part = input("Enter email or part of email: ").strip()

    if not email_part:
        print("Search text cannot be empty.")
        return

    contacts = get_contacts(
        "WHERE c.email ILIKE %s",
        (f"%{email_part}%",)
    )

    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        display_contact(contact)


# ==========================================
# 7. SORT CONTACTS
# ==========================================

def sort_contacts():
    print("\n1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose sorting option: ").strip()

    options = {
        "1": ("name", "Name"),
        "2": ("birthday", "Birthday"),
        "3": ("created_at", "Date added")
    }

    if choice not in options:
        print("Invalid option.")
        return

    sort_by, title = options[choice]
    contacts = get_contacts(sort_by=sort_by)

    print(f"\n========== SORTED BY {title.upper()} ==========")

    for contact in contacts:
        display_contact(contact)


# ==========================================
# 8. PAGINATION
# ==========================================

def paginated_contacts():
    page_size = 3
    current_page = 0

    while True:
        connection = connect()

        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    c.id,
                    c.first_name,
                    c.email,
                    c.birthday,
                    g.name,
                    c.created_at,
                    ARRAY(
                        SELECT ARRAY[p.phone, p.type]
                        FROM phones p
                        WHERE p.contact_id = c.id
                        ORDER BY p.id
                    )
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY c.id
                LIMIT %s OFFSET %s;
            """, (page_size, current_page * page_size))

            contacts = cursor.fetchall()

        except Exception as error:
            print("Database error:", error)
            return

        finally:
            cursor.close()
            connection.close()

        if not contacts and current_page == 0:
            print("PhoneBook is empty.")
            return

        if not contacts:
            print("No more contacts.")
            current_page -= 1
            continue

        print(f"\n========== PAGE {current_page + 1} ==========")

        for contact in contacts:
            display_contact(contact)

        command = input(
            "\nEnter next, prev or quit: "
        ).strip().lower()

        if command == "next":
            current_page += 1
        elif command == "prev":
            if current_page > 0:
                current_page -= 1
            else:
                print("Already on the first page.")
        elif command == "quit":
            break
        else:
            print("Invalid command.")


# ==========================================
# 9. EXPORT TO JSON
# ==========================================

def export_to_json():
    connection = connect()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                c.id,
                c.first_name,
                c.email,
                c.birthday,
                g.name,
                c.created_at,
                ARRAY(
                    SELECT ARRAY[p.phone, p.type]
                    FROM phones p
                    WHERE p.contact_id = c.id
                    ORDER BY p.id
                )
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id;
        """)

        contacts = cursor.fetchall()
        data = []

        for contact in contacts:
            data.append({
                "id": contact[0],
                "name": contact[1],
                "email": contact[2],
                "birthday": (
                    contact[3].isoformat()
                    if contact[3] else None
                ),
                "group": contact[4],
                "created_at": (
                    contact[5].isoformat()
                    if contact[5] else None
                ),
                "phones": [
                    {
                        "number": phone[0],
                        "type": phone[1]
                    }
                    for phone in (contact[6] or [])
                ]
            })

        file_path = os.path.join(
            os.path.dirname(__file__),
            "contacts.json"
        )

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Contacts exported successfully!")

    except Exception as error:
        print("Export error:", error)

    finally:
        cursor.close()
        connection.close()


# ==========================================
# 10. IMPORT FROM JSON
# ==========================================

def import_from_json():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "contacts.json"
    )

    if not os.path.exists(file_path):
        print("JSON file not found. Export contacts first.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid JSON format.")
            return

    except Exception as error:
        print("File reading error:", error)
        return

    connection = connect()

    if connection is None:
        return

    cursor = connection.cursor()
    imported = 0
    skipped = 0
    overwritten = 0

    try:
        for item in data:
            name = str(item.get("name") or "").strip()
            phones = item.get("phones", [])

            if not name or not isinstance(phones, list):
                skipped += 1
                continue

            valid_phones = []

            for phone in phones:
                if not isinstance(phone, dict):
                    continue

                number = str(phone.get("number") or "").strip()
                phone_type = str(
                    phone.get("type") or "mobile"
                ).lower().strip()

                if number and phone_type in ("home", "work", "mobile"):
                    valid_phones.append((number, phone_type))

            if not valid_phones:
                skipped += 1
                continue

            group_name = item.get("group")
            group_id = None

            if group_name:
                cursor.execute("""
                    SELECT id FROM groups
                    WHERE name ILIKE %s LIMIT 1;
                """, (group_name,))

                result = cursor.fetchone()

                if result:
                    group_id = result[0]
                else:
                    cursor.execute("""
                        INSERT INTO groups (name)
                        VALUES (%s) RETURNING id;
                    """, (group_name,))
                    group_id = cursor.fetchone()[0]

            email = item.get("email") or None
            birthday = item.get("birthday") or None

            if birthday:
                date.fromisoformat(birthday)

            cursor.execute("""
                SELECT id FROM contacts
                WHERE first_name ILIKE %s
                ORDER BY id LIMIT 1;
            """, (name,))

            existing = cursor.fetchone()

            if existing:
                print(f"\nContact '{name}' already exists.")
                action = input(
                    "Enter skip or overwrite: "
                ).strip().lower()

                if action == "skip":
                    skipped += 1
                    continue

                if action != "overwrite":
                    print("Invalid choice. Skipping.")
                    skipped += 1
                    continue

                contact_id = existing[0]

                cursor.execute("""
                    UPDATE contacts
                    SET phone = %s,
                        email = %s,
                        birthday = %s,
                        group_id = %s
                    WHERE id = %s;
                """, (
                    valid_phones[0][0],
                    email,
                    birthday,
                    group_id,
                    contact_id
                ))

                cursor.execute(
                    "DELETE FROM phones WHERE contact_id = %s",
                    (contact_id,)
                )

                for number, phone_type in valid_phones:
                    cursor.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s);
                    """, (contact_id, number, phone_type))

                overwritten += 1

            else:
                cursor.execute("""
                    INSERT INTO contacts
                        (first_name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    name,
                    valid_phones[0][0],
                    email,
                    birthday,
                    group_id
                ))

                contact_id = cursor.fetchone()[0]

                for number, phone_type in valid_phones:
                    cursor.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s);
                    """, (contact_id, number, phone_type))

                imported += 1

        connection.commit()

        print("\n========== IMPORT SUMMARY ==========")
        print("New contacts imported:", imported)
        print("Contacts overwritten:", overwritten)
        print("Contacts skipped:", skipped)
        print("Import completed!")

    except Exception as error:
        connection.rollback()
        print("Import error:", error)

    finally:
        cursor.close()
        connection.close()


# ==========================================
# 11. IMPORT FROM CSV
# ==========================================

def import_from_csv():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "contacts.csv"
    )

    if not os.path.exists(file_path):
        print("CSV file not found.")
        return

    connection = connect()

    if connection is None:
        return

    cursor = connection.cursor()
    imported = 0
    skipped = 0

    required_columns = {
        "first_name",
        "phone",
        "phone_type",
        "email",
        "birthday",
        "group"
    }

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                print("Invalid CSV headers.")
                print("Required:", ", ".join(sorted(required_columns)))
                return

            for row in reader:
                name = (row.get("first_name") or "").strip()
                phone = (row.get("phone") or "").strip()
                phone_type = (
                    row.get("phone_type") or "mobile"
                ).strip().lower()

                email = (row.get("email") or "").strip() or None
                birthday = (row.get("birthday") or "").strip() or None
                group_name = (row.get("group") or "").strip()

                if not name or not phone:
                    print("Skipping row: name or phone is missing.")
                    skipped += 1
                    continue

                if phone_type not in ("home", "work", "mobile"):
                    print(f"Skipping {name}: invalid phone type.")
                    skipped += 1
                    continue

                if birthday:
                    try:
                        date.fromisoformat(birthday)
                    except ValueError:
                        print(f"Skipping {name}: invalid birthday.")
                        skipped += 1
                        continue

                cursor.execute("""
                    SELECT id FROM contacts
                    WHERE first_name ILIKE %s
                    LIMIT 1;
                """, (name,))

                if cursor.fetchone():
                    print(f"Skipping {name}: already exists.")
                    skipped += 1
                    continue

                group_id = None

                if group_name:
                    cursor.execute("""
                        SELECT id FROM groups
                        WHERE name ILIKE %s LIMIT 1;
                    """, (group_name,))

                    result = cursor.fetchone()

                    if result:
                        group_id = result[0]
                    else:
                        cursor.execute("""
                            INSERT INTO groups (name)
                            VALUES (%s) RETURNING id;
                        """, (group_name,))
                        group_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO contacts
                        (first_name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    name,
                    phone,
                    email,
                    birthday,
                    group_id
                ))

                contact_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s);
                """, (contact_id, phone, phone_type))

                imported += 1

        connection.commit()

        print("\n========== CSV IMPORT SUMMARY ==========")
        print("New contacts imported:", imported)
        print("Contacts skipped:", skipped)
        print("CSV import completed!")

    except Exception as error:
        connection.rollback()
        print("CSV import error:", error)

    finally:
        cursor.close()
        connection.close()


# ==========================================
# 12. ADD PHONE USING SQL PROCEDURE
# ==========================================

def add_phone():
    name = input("Enter contact name: ").strip()
    phone = input("Enter new phone number: ").strip()
    phone_type = input(
        "Enter phone type (home/work/mobile): "
    ).strip().lower()

    if phone_type not in ("home", "work", "mobile"):
        print("Invalid phone type.")
        return

    connection = connect()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            "CALL add_phone(%s, %s, %s);",
            (name, phone, phone_type)
        )
        connection.commit()
        print("Phone added successfully!")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


# ==========================================
# 13. MOVE CONTACT TO GROUP
# ==========================================

def move_to_group():
    name = input("Enter contact name: ").strip()
    group_name = input("Enter new group name: ").strip()

    connection = connect()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            "CALL move_to_group(%s, %s);",
            (name, group_name)
        )
        connection.commit()
        print("Contact moved to group successfully!")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


# ==========================================
# 14. SEARCH USING SQL FUNCTION
# ==========================================

def search_contacts():
    query = input("Enter name, email or phone: ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    connection = connect()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT * FROM search_contacts(%s);",
            (query,)
        )

        results = cursor.fetchall()

        if not results:
            print("No matching contacts found.")
            return

        print("\n========== SEARCH RESULTS ==========")

        for result in results:
            print("\n----------------------------------------")
            print("ID:", result[0])
            print("Name:", result[1])
            print("Email:", result[2] or "Not specified")
            print("Birthday:", result[3] or "Not specified")
            print("Group:", result[4] or "Not specified")
            print("Phones:", result[5] or "None")
            print("----------------------------------------")

    except Exception as error:
        print("Search error:", error)

    finally:
        cursor.close()
        connection.close()


# ==========================================
# 15. MAIN MENU
# ==========================================

def main():
    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Show all contacts")
        print("2. Add contact")
        print("3. Filter contacts by group")
        print("4. Search contacts by email")
        print("5. Sort contacts")
        print("6. Browse contacts by pages")
        print("7. Export contacts to JSON")
        print("8. Import contacts from JSON")
        print("9. Import contacts from CSV")
        print("10. Add phone using procedure")
        print("11. Move contact to group")
        print("12. Search using SQL function")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            show_contacts()

        elif choice == "2":
            add_contact()

        elif choice == "3":
            filter_by_group()

        elif choice == "4":
            search_by_email()

        elif choice == "5":
            sort_contacts()

        elif choice == "6":
            paginated_contacts()

        elif choice == "7":
            export_to_json()

        elif choice == "8":
            import_from_json()

        elif choice == "9":
            import_from_csv()

        elif choice == "10":
            add_phone()

        elif choice == "11":
            move_to_group()

        elif choice == "12":
            search_contacts()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


# ==========================================
# 16. RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
