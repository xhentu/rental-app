import sqlite3
import os

def inspect_db():
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names, excluding Django internal metadata tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'django_%' 
        AND name NOT LIKE 'auth_%' AND name NOT LIKE 'sqlite_%';
    """)
    tables = cursor.fetchall()

    print(f"\n{'='*50}")
    print(f"   DATABASE SCHEMA: {db_path}")
    print(f"{'='*50}\n")

    for table in tables:
        table_name = table[0]
        print(f"🔹 TABLE: {table_name}")
        print(f"{'-'*30}")
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for col in columns:
            # col[1] = name, col[2] = type, col[3] = nullable, col[5] = PK
            pk = "[PK]" if col[5] else ""
            nullable = "NULL" if col[3] == 0 else "NOT NULL"
            print(f"  • {col[1]:<20} | {col[2]:<10} | {nullable} {pk}")
        print("\n")

    conn.close()

if __name__ == "__main__":
    inspect_db()