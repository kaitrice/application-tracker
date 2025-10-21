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
		title TEXT NOT NULL,
		addr1 TEXT,
		addr2 TEXT,
		city TEXT,
		date TEXT,
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