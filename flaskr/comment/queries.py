

def comment_list(db, post_id):
    return db.execute(
        "SELECT c.id, c.body, c.created, post_id, title, c.author_id, username"
        " FROM (comment c JOIN post p ON c.post_id = p.id)"
        " JOIN user u ON c.author_id = u.id"
        " WHERE post_id = ?"
        " ORDER BY c.created DESC",
        (post_id,),
    ).fetchall()


def get_comment(db, post_id, comment_id):
    return db.execute(
        "SELECT c.id, c.body, c.created, post_id, title, c.author_id, username"
        " FROM (comment c JOIN post p ON c.post_id = p.id)"
        " JOIN user u ON c.author_id = u.id"
        " WHERE (post_id = ?) AND (c.id = ?)",
        (post_id, comment_id),
    ).fetchone()


def get_last_id(db):
    return db.execute(
        "SELECT last_insert_rowid() FROM comment",
    ).fetchone()


def create_comment(db, body, post_id, author_id):
    db.execute(
        "INSERT INTO comment (post_id, body, author_id) VALUES (?, ?, ?)",
        (post_id, body, author_id),
    )
    db.commit()


def update_comment(db, body, post_id, comment_id):
    db.execute(
        "UPDATE comment"
        " SET body = ?"
        " WHERE (post_id = ?) AND (id = ?)",
        (body, post_id, comment_id),
    )
    db.commit()


def delete_comment(db, post_id, comment_id):
    db.execute(
        "DELETE FROM comment"
        " WHERE (post_id = ?) AND (id = ?)",
        (post_id, comment_id,)
    )
    db.commit()
