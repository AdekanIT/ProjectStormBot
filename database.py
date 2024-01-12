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
            'pr_des TEXT, pr_count INTEGER, pr_photo TEXT, pr_price REAL);')

# Table for products in box
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(user_id INTEGER, user_product TEXT, pr_amount INTEGER, total REAL);')

# Register for clients
def register(id, username, phon_num, location):
    sql.execute('INSERT INTO users(id, username, phon_num, location) VALUES(?, ?, ?, ?);',
                (id, username, phon_num, location))
    # Save our changes
    base.commit()

# Check for exist user in base
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False

# Method for take all information about products
def get_pr(id):
    result = sql.execute('SELECT pr_name, pr_des, pr_count, pr_photo, pr_price FROM products WHERE id=?;', (id,))
    return result.fetchone()

# Method for show product in buttons
def get_pr_but():
    return sql.execute('SELECT id, pr_name, pr_count FROM products;').fetchall()

# Method for add product
def add_pr(name, des, count, photo, price):
    sql.execute('INSERT INTO products(pr_name, pr_des, pr_count, pr_photo, pr_price) '
                'VALUES(?, ?, ?, ?, ?);', (name, des, count, photo, price))
    # Save changes
    base.commit()

# Method for delete products
def del_pr(id):
    sql.execute('DELETE FROM products WHERE id=?;', (id, ))
    # Save changes
    base.commit()

# Method for change product count
def change_pr_count(id, new_count):
    # Current current product
    now_count = sql.execute('SELECT pr_count FROM products WHERE id=?;', (id, )).fetchone()
    # New product count
    plus_count = now_count[0] + new_count
    sql.execute('UPDATE products SET pr_count=? WHERE id=?;', (plus_count, id))
    # Save changes
    base.commit()

# Methods for cart
# Method for add product in cart
def add_pr_cart(user_id, user_product, pr_amount, total):
    sql.execute('INSERT INTO cart VALUES(?, ?, ?, ?);', (user_id, user_product, pr_amount, total))
    # Save changes
    base.commit()

def get_pr_name_id():
    prods = sql.execute('SELECT id, pr_count FROM products;').fetchall()
    all_prods = [i[0] for i in prods if i[1] > 0]
    return all_prods

def check_pr():
    if sql.execute('SELECT * FROM products').fetchall():
        return True
    else:
        return False


def check_pr_id(id):
    if sql.execute('SELECT id FROM products WHERE id=?;', (id, )).fetchone():
        return True
    else:
        return False

# Clear cart
def clear_cart(user_id):
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id, ))
    base.commit()


def check_cart(id):
    if sql.execute('SELECT user_product FROM cart WHERE user_id=?;', (id, )).fetchall():
        return True
    else:
        return False

#  Get order
def make_order(user_id):
    pr_name = sql.execute('SELECT user_product FROM cart WHERE user_id=?;', (user_id, )).fetchone()
    amount = sql.execute('SELECT pr_amount FROM cart WHERE user_id=?;', (user_id, )).fetchone()
    pr_quantity = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;', (pr_name[0], )).fetchone()
    new_quantity = pr_quantity[0] - amount[0]
    sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;', (new_quantity, pr_name[0]))
    info = sql.execute('SELECT * FROM cart WHERE user_id=?;', (user_id, )).fetchone()
    address = sql.execute('SELECT location FROM users WHERE id=?;', (user_id, )).fetchone()
    # Save changes
    base.commit()
    return info, address

# Show cart
def show_cart(user_id):
    return sql.execute('SELECT user_product, pr_amount, total FROM cart WHERE user_id=?;', (user_id, )).fetchone()




















