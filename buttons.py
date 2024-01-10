from telebot import types

# Button for sent phone number
def num_bt():
    # Create environment
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Create button
    number = types.KeyboardButton('Sent phone number', request_contact=True)
    # Add button in environment
    kb.add(number)
    return kb

# Buttons for sent location
def loc_bt():
    # Create environment
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Create button
    location = types.KeyboardButton('Sent location', request_location=True)
    # Add button in environment
    kb.add(location)
    return kb

#  Buttons for choice product
def main_memu_buttons(pr_from_db):
    # Create environment
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Create buttons
    cart = types.InlineKeyboardButton(callback_data='cart', text='Cart')
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}') for i in pr_from_db
                    if i[2] > 0]
    # Add buttons in environment
    kb.add(*all_products)
    kb.row(cart)

# Button for choice count
def choice_pr_count(amount=1, plus_or_minus=''):
    # Create environment
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Create buttons
    back = types.InlineKeyboardButton(callback_data='back', text='Back')
    to_cart = types.InlineKeyboardButton(callback_data='to_cart', text='Add to Cart')
    plus = types.InlineKeyboardButton(callback_data='increment', text='+')
    minus = types.InlineKeyboardButton(callback_data='decrement', text='-')
    count = types.InlineKeyboardButton(callback_data=str(amount), text=str(amount))
    # Algorithm for add and delete count of product
    if plus_or_minus == 'increment':
        new_amount = int(amount)+1
        count = types.InlineKeyboardButton(callback_data=str(new_amount), text=str(new_amount))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            new_amount = int(amount) - 1
            count = types.InlineKeyboardButton(callback_data=str(new_amount), text=str(new_amount))
    # Add buttons in environment
    kb.add(minus, count, plus)
    kb.row(back, to_cart)
    return kb

# Buttons for admin
# Menu admin
def admin_menu():
    # Create environment
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Create buttons
    but1 = types.KeyboardButton('Add product')
    but2 = types.KeyboardButton('Delete product')
    but3 = types.KeyboardButton('Change product')
    but4 = types.KeyboardButton('Go to menu')
    # Add buttons in environment
    kb.add(but1, but2, but3)
    kb.row(but4)
    return kb

# Button for conform
def confirm():
    # Create environment
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Create buttons
    but1 = types.KeyboardButton('Yes')
    but2 = types.KeyboardButton('No')
    # Add buttons in environment
    kb.add(but1, but2)
    return kb





