import json
import sqlite3


DB_PATH = 'data/database.db'

def execute(query: str, params: tuple = (), commit: bool = False):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # TODO: validate query
            cursor.execute(query, params)
                
            if commit:
                conn.commit()
                
            if query.strip().lower().startswith('select'):
                return cursor.fetchAll()
    except sqlite3.Error as e:
        print(f'Database error: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

def init_db():
    companies_schema = """
    CREATE TABLE IF NOT EXISTS companies (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		addr1 TEXT,
		addr2 TEXT,
		city TEXT,
		state TEXT,
		zip TEXT,
		phone_number TEXT
	);
    """
    applications_schema = """
    CREATE TABLE IF NOT EXISTS applications (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		company_id INTEGER NOT NULL,
		position TEXT NOT NULL,
		status TEXT DEFAULT 'applied',
		date_applied DATE DEFAULT CURRENT_DATE,
		notes TEXT,
        FOREIGN KEY (company_id) REFERENCES companies(id)
	);
    """
    contacts_schema = """
    CREATE TABLE IF NOT EXISTS contacts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		company_id INTEGER NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
		title TEXT NOT NULL,
		status TEXT,
		date_contacted DATE,
        FOREIGN KEY (company_id) REFERENCES companies(id)
	);
    """
    try:
        execute(companies_schema, commit=True)
        execute(applications_schema, commit=True)
        execute(contacts_schema, commit=True)
        print("Database initialized.")
    except sqlite3.Error as e:
        print(f'Database setup error: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

def seed_db(json_file: str = 'data/test_data.json'):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    execute("DELETE FROM applications;", commit=True)
    execute("DELETE FROM contacts;", commit=True)
    execute("DELETE FROM companies;", commit=True)

    for company in data.get("companies"):
        execute(
			"""
			INSERT INTO companies (id, name, addr1, addr2, city, state, zip, phone_number)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?);
			""",
			(
				company["id"],
				company["name"],
				company["addr1"],
				company["addr2"],
				company["city"],
				company["state"],
				company["zip"],
				company["phone_number"]
			),
			commit=True
		)
    
    for application in data.get("applications"):
        execute(
			"""
			INSERT INTO applications (id, company_id, position, status, date_applied, notes)
			VALUES (?, ?, ?, ?, ?, ?);
			""",
			(
				application["id"],
				application["company_id"],
				application["position"],
				application["status"],
				application["date_applied"],
				application["notes"]
			),
			commit=True
		)

    for contact in data.get("contacts"):
        execute(
			"""
			INSERT INTO contacts (id, company_id, first_name, last_name, title, status, date_contacted)
			VALUES (?, ?, ?, ?, ?, ?, ?);
			""",
			(
				contact["id"],
				contact["company_id"],
				contact["first_name"],
				contact["last_name"],
				contact["title"],
				contact["status"],
				contact["date_contacted"]
			),
			commit=True
		)
    
    print('Database seeded.')