
-- =========================================
-- 1. PROCEDURE: add_phone
-- Add a new phone number to an existing contact
-- =========================================

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_count INTEGER;
    v_type VARCHAR;
BEGIN
    IF p_contact_name IS NULL OR TRIM(p_contact_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;

    IF p_phone IS NULL OR TRIM(p_phone) = '' THEN
        RAISE EXCEPTION 'Phone number cannot be empty';
    END IF;

    v_type := LOWER(TRIM(p_type));

    IF v_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type: %. Use home, work or mobile', v_type;
    END IF;

    SELECT COUNT(*), MIN(id)
    INTO v_count, v_contact_id
    FROM contacts
    WHERE first_name ILIKE TRIM(p_contact_name);

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    ELSIF v_count > 1 THEN
        RAISE EXCEPTION 'More than one contact has this name';
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, TRIM(p_phone), v_type);
END;
$$;


-- =========================================
-- 2. PROCEDURE: move_to_group
-- Move a contact to another group
-- Create the group if it does not exist
-- =========================================

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
    v_count INTEGER;
    v_normalized_group VARCHAR;
BEGIN
    IF p_contact_name IS NULL OR TRIM(p_contact_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;

    IF p_group_name IS NULL OR TRIM(p_group_name) = '' THEN
        RAISE EXCEPTION 'Group name cannot be empty';
    END IF;

    SELECT COUNT(*), MIN(id)
    INTO v_count, v_contact_id
    FROM contacts
    WHERE first_name ILIKE TRIM(p_contact_name);

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    ELSIF v_count > 1 THEN
        RAISE EXCEPTION 'More than one contact has this name';
    END IF;

    v_normalized_group := INITCAP(LOWER(TRIM(p_group_name)));

    INSERT INTO groups (name)
    VALUES (v_normalized_group)
    ON CONFLICT (name)
    DO UPDATE SET name = EXCLUDED.name
    RETURNING id INTO v_group_id;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;


-- =========================================
-- 3. FUNCTION: search_contacts
-- Search by name, email and all phone numbers
-- =========================================

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    first_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone_numbers TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_query IS NULL OR TRIM(p_query) = '' THEN
        RAISE EXCEPTION 'Search query cannot be empty';
    END IF;

    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.email,
        c.birthday,
        g.name,
        COALESCE(
            STRING_AGG(
                p.phone || ' (' || p.type || ')',
                ', ' ORDER BY p.id
            ),
            ''
        )
    FROM contacts c
    LEFT JOIN groups g
        ON c.group_id = g.id
    LEFT JOIN phones p
        ON c.id = p.contact_id
    WHERE
        c.first_name ILIKE '%' || TRIM(p_query) || '%'
        OR COALESCE(c.email, '') ILIKE '%' || TRIM(p_query) || '%'
        OR EXISTS (
            SELECT 1
            FROM phones p2
            WHERE p2.contact_id = c.id
              AND p2.phone ILIKE '%' || TRIM(p_query) || '%'
        )
    GROUP BY
        c.id, c.first_name, c.email,
        c.birthday, g.name
    ORDER BY c.first_name;
END;
$$;
