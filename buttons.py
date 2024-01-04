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