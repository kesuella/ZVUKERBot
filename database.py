import aiosqlite

DB_PATH = "voice_data.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS voices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                file_id TEXT,
                user_id INTEGER,
                is_approved INTEGER DEFAULT 0
            )
        ''')
        await db.commit()

async def add_voice(keyword, file_id, user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO voices (keyword, file_id, user_id, is_approved) VALUES (?, ?, ?, 0)",
            (keyword, file_id, user_id)
        )
        await db.commit()

async def approve_voice(voice_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE voices SET is_approved = 1 WHERE id = ?", (voice_id,))
        await db.commit()

async def get_pending_voices():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id, keyword, file_id FROM voices WHERE is_approved = 0")
        return await cursor.fetchall()

async def search_voices(query):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT file_id FROM voices WHERE is_approved = 1 AND keyword LIKE ?",
            (f"%{query}%",)
        )
        return await cursor.fetchall()

async def delete_voice_by_file_id(file_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM voices WHERE file_id = ?", (file_id,))
        await db.commit()