import sqlite3

# Connection to Base
base = sqlite3.connect("stormstore.db", check_same_thread=False)
# Python + SQL
sql = base.cursor()

# Table for users
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(id INTEGER, username TEXT, phon_num TEXT, location TEXT);')

# Table for products
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, '
            'pd_des TEXT, pr_count INTEGER, pr_photo TEXT, pr_price REAL);')

# Table for products in box
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(user_id INTEGER, user_product TEXT, pr_amount INTEGER, total REAL);')

# Register for clients
def register(id, username, phon_num, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, username, phon_num, location))
    # Save our changes
    base.commit()

# Check for exist user in base
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False















