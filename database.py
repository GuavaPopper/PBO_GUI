import sqlite3

class Database:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_file TEXT NOT NULL,
            lokasi_file TEXT NOT NULL,
            teks_input TEXT,
            hasil_ekstraksi TEXT,
            tanggal TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()

# Contoh penggunaan
if __name__ == "__main__":
    db = Database()
    print("Database dan tabel berhasil dibuat.")
    db.close()
