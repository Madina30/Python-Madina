
-- 1. Create contact groups
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Insert default groups
INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

-- 3. Extend existing contacts table
ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS email VARCHAR(100),
ADD COLUMN IF NOT EXISTS birthday DATE,
ADD COLUMN IF NOT EXISTS group_id INTEGER
    REFERENCES groups(id),
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- 4. Create phones table
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL
        REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(30) NOT NULL,
    type VARCHAR(10) NOT NULL
        CHECK (type IN ('home', 'work', 'mobile'))
);

-- 5. Move existing phone numbers to the new table
INSERT INTO phones (contact_id, phone, type)
SELECT c.id, c.phone, 'mobile'
FROM contacts c
WHERE c.phone IS NOT NULL
  AND TRIM(c.phone) <> ''
  AND NOT EXISTS (
      SELECT 1
      FROM phones p
      WHERE p.contact_id = c.id
        AND p.phone = c.phone
  );

-- 6. Create indexes
CREATE INDEX IF NOT EXISTS idx_phones_contact_id
ON phones(contact_id);

CREATE INDEX IF NOT EXISTS idx_contacts_group_id
ON contacts(group_id);
