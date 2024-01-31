import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect('tg1.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id INTEGER, "
                "cart_id TEXT )")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "  # "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "desc TEXT, "
                "price TEXT, "
                "photo TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS category("
                "c_id INTEGER PRIMARY KEY AUTOINCREMENT, "  # "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS korzina ("
                "user_id VARCHAR(99999) NULL,"
                "item TEXT DEFAULT NULL,"
                "price TEXT)")
    db.commit()


async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()


def delete_item(id):
    db = sq.connect('tg1.db')
    cur = db.cursor()
    sql_query = "DELETE FROM items WHERE i_id = ?"
    cur.execute(sql_query, (id,))
    print("its over")

    db.commit()
    db.close()


def delete_item1(ссid):
    db = sq.connect('tg1.db')
    cur = db.cursor()
    sql_query = "DELETE FROM category WHERE c_id = ?"
    cur.execute(sql_query, (ссid,))
    print("its over")

    db.commit()
    db.close()


def add_item(desc, price, photo):
    cur.execute(
        'INSERT INTO ITEMS ( desc, price, photo) VALUES(?, ?, ?)',
        ( desc, price, photo)
    )
    db.commit()


def add_item1(name):
    db = sq.connect('tg1.db')
    cur = db.cursor()

    cur.execute("INSERT INTO category (name) VALUES(?)", (name,))

    db.commit()


def add_kor(user_id, item,price):
    cur.execute('INSERT INTO korzina (user_id, item,price) VALUES(?,?,?)', (user_id, item,price))
    db.commit()


def ud_kor(user_id):
    db = sq.connect('tg1.db')
    cur = db.cursor()
    sql_query = "DELETE FROM korzina WHERE user_id = ?"
    cur.execute(sql_query, (user_id,))
    db.commit()
