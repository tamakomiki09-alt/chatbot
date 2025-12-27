import sqlite3

DB_NAME = "chatbot.db"

def get_connection():
    """Returns a connection to the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # allows dict-like access
    return conn


def save_message(session_id, user_msg, ai_msg, category=None,
                 keywords=None, interest=None, time_pref=None,
                 mobility=None, escalated=False):
    """Inserts a conversation entry into the database."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO conversations (
            session_id, user_message, ai_response, category,
            keywords, interest_pref, time_pref, mobility_pref, escalated
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (session_id, user_msg, ai_msg, category, keywords,
          interest, time_pref, mobility, escalated))

    conn.commit()
    conn.close()


def get_all_messages():
    """Returns all stored conversation rows."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM conversations ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
