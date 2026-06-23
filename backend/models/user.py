from db.db import get_db

def create_tables():
    conn=get_db()
    cursor=conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE, 
        email TEXT NOT NULL UNIQUE,
         
        community_saver BOOLEAN NOT NULL,

        password TEXT NOT NULL

        )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS friends(
    user_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (friend_id) REFERENCES users(id),
    PRIMARY KEY (user_id, friend_id)

    )

    """
    )

    conn.commit()
    conn.close()

    print("table create ")