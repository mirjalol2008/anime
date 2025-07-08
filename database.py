import sqlite3

def init_db():
    conn = sqlite3.connect("anime.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS collections (
        id TEXT PRIMARY KEY,
        created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collection_id TEXT,
        file_id TEXT,
        FOREIGN KEY(collection_id) REFERENCES collections(id)
    )''')
    conn.commit()
    conn.close()

def create_collection(collection_id):
    conn = sqlite3.connect("anime.db")
    c = conn.cursor()
    c.execute("INSERT INTO collections (id, created_at) VALUES (?, datetime('now'))", (collection_id,))
    conn.commit()
    conn.close()

def add_file_to_collection(collection_id, file_id):
    conn = sqlite3.connect("anime.db")
    c = conn.cursor()
    c.execute("INSERT INTO files (collection_id, file_id) VALUES (?, ?)", (collection_id, file_id))
    conn.commit()
    conn.close()

def get_files_by_collection(collection_id):
    conn = sqlite3.connect("anime.db")
    c = conn.cursor()
    c.execute("SELECT file_id FROM files WHERE collection_id = ?", (collection_id,))
    files = [row[0] for row in c.fetchall()]
    conn.close()
    return files