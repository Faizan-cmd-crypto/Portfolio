from app import create_app
from models import db
import sqlite3
import os
import json
from datetime import datetime

def backup_data():
    """Backup all data from the database."""
    app = create_app()
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not db_path.startswith('/'):
            db_path = os.path.join(app.root_path, db_path)
        
        # Create backups directory if it doesn't exist
        backup_dir = os.path.join(app.root_path, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Create backup data structure
        backup = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            backup[table_name] = {
                'columns': columns,
                'data': rows
            }
        
        # Save backup to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
        with open(backup_file, 'w') as f:
            json.dump(backup, f, default=str)
        
        print(f"Backup created at: {backup_file}")
        conn.close()
        return backup_file

def restore_data(backup_file):
    """Restore data from backup file."""
    app = create_app()
    with app.app_context():
        with open(backup_file, 'r') as f:
            backup = json.load(f)
        
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not db_path.startswith('/'):
            db_path = os.path.join(app.root_path, db_path)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        for table_name, table_data in backup.items():
            columns = table_data['columns']
            data = table_data['data']
            
            # Skip sqlite_sequence table
            if table_name == 'sqlite_sequence':
                continue
            
            # Prepare SQL statement
            placeholders = ','.join(['?' for _ in columns])
            column_names = ','.join(columns)
            sql = f"INSERT OR REPLACE INTO {table_name} ({column_names}) VALUES ({placeholders})"
            
            # Insert data
            for row in data:
                try:
                    cursor.execute(sql, row)
                except sqlite3.Error as e:
                    print(f"Error restoring row in {table_name}: {e}")
                    continue
        
        conn.commit()
        conn.close()
        print("Data restored successfully!")

def add_resume_file_column():
    """Add resume_file column to the profile table."""
    app = create_app()
    with app.app_context():
        # First, create a backup
        backup_file = backup_data()
        
        # Get database path
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not db_path.startswith('/'):
            db_path = os.path.join(app.root_path, db_path)
        
        print(f"Database path: {db_path}")
        
        try:
            # Connect to SQLite database directly
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # List all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Available tables:", [table[0] for table in tables])
            
            # Find the profile table
            profile_table = None
            for table in tables:
                if table[0].lower() == 'profile':
                    profile_table = table[0]
                    break
            
            if not profile_table:
                raise Exception("Profile table not found!")
            
            # Check if column already exists
            cursor.execute(f"PRAGMA table_info({profile_table})")
            columns = [column[1] for column in cursor.fetchall()]
            print(f"Existing columns in {profile_table}:", columns)
            
            if 'resume_file' not in columns:
                print(f"Adding 'resume_file' column to {profile_table} table...")
                cursor.execute(f"ALTER TABLE {profile_table} ADD COLUMN resume_file TEXT")
                conn.commit()
                print("Column added successfully!")
            else:
                print("Column 'resume_file' already exists.")
            
            conn.close()
            
            # Restore the data
            restore_data(backup_file)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Attempting to restore from backup...")
            restore_data(backup_file)

if __name__ == '__main__':
    add_resume_file_column() 