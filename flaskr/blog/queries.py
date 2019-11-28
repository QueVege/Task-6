

def post_list(db):
    return db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC",
    ).fetchall()


def get_post(db, id):
    return db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = ?",
        (id,),
    ).fetchone()


def get_last_id(db):
    return db.execute(
        "SELECT last_insert_rowid() FROM post",
    ).fetchone()


def create_post(db, title, body, author_id):
    db.execute(
        "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
        (title, body, author_id),
    )
    db.commit()


def update_post(db, title, body, id):
    db.execute(
        "UPDATE post"
        " SET title = ?, body = ?"
        " WHERE id = ?",
        (title, body, id),
    )
    db.commit()


def delete_post(db, id):
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
