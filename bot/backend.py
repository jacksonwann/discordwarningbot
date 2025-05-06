import sqlite3

class Database:
    """SQLite-backed warning database with thread-safe access."""

    def __init__(self):
        self.conn = sqlite3.connect("warnings.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                user_id TEXT,
                reason TEXT
            )
        ''')
        self.conn.commit()

    def add_warning(self, user_id, reason):
        """Add a warning for a user."""
        self.cursor.execute(
            'INSERT INTO warnings (user_id, reason) VALUES (?, ?)',
            (str(user_id), reason)
        )
        self.conn.commit()

    def get_warnings(self, user_id):
        """Retrieve a list of warning reasons for a user."""
        self.cursor.execute(
            'SELECT reason FROM warnings WHERE user_id = ?',
            (str(user_id),)
        )
        return [row[0] for row in self.cursor.fetchall()]

    def clear_warnings(self, user_id):
        """Delete all warnings for a given user."""
        self.cursor.execute(
            'DELETE FROM warnings WHERE user_id = ?',
            (str(user_id),)
        )
        self.conn.commit()