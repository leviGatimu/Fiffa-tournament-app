import sqlite3

def upgrade_database():
    print("🚑 Attempting to save your database...")
    
    try:
        # Connect to your existing database
        conn = sqlite3.connect('fifa_tournament.db')
        cursor = conn.cursor()
        
        # 1. Add the missing 'logo' column
        try:
            print("Attempting to add 'logo' column...")
            cursor.execute("ALTER TABLE player ADD COLUMN logo TEXT DEFAULT ''")
            print("✅ 'logo' column added successfully.")
        except sqlite3.OperationalError:
            print("ℹ️ 'logo' column already exists (Skipping).")

        # 2. Add the missing 'clean_sheets' column
        try:
            print("Attempting to add 'clean_sheets' column...")
            cursor.execute("ALTER TABLE player ADD COLUMN clean_sheets INTEGER DEFAULT 0")
            print("✅ 'clean_sheets' column added successfully.")
        except sqlite3.OperationalError:
            print("ℹ️ 'clean_sheets' column already exists (Skipping).")

        conn.commit()
        conn.close()
        print("\n🎉 SUCCESS! Your database is updated. You kept all your players!")
        print("You can now run 'python app.py' safely.")
        
    except Exception as e:
        print(f"\n❌ Something went wrong: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    upgrade_database()