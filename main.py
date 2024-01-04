import telebot
import database as db
import buttons as bt
from geopy import Nominatim

# Create bot object
bot = telebot.TeleBot('6886952357:AAEVGO1qD-1Zefk7YG-CpkTuGas4w9cFP0k')
# Use map
geolocation = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                   '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
# Command /start in bot
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Check user
    check = db.checker(user_id)
    #  If check = True
    if check:
        bot.send_message(user_id, f'Hello {message.from_user.first_name}!'
                                  'Welcome back to our Storm Store or short format SS')
    else:
        bot.send_message(user_id, f'Hello {message.from_user.first_name}!\n'
                         "Welcome to our Storm Store or short format SS"
                         "Let's registrate you in Store base!\n"
                         "Please enter your name")
        # Link to take name
        bot.register_next_step_handler(message, get_name)

# Step to take name
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Great! Now please send your number!',
                     reply_markup=bt.num_bt())
    # Link to take phone number
    bot.register_next_step_handler(message, get_number, name)

# Step to take phone number
def get_number(message, name):
    user_id = message.from_user.id
    # If user sent number by button
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Incredible! Last step, please send your location',
                         reply_markup=bt.loc_bt())
        # Link for take location
        bot.register_next_step_handler(message, get_location, name, number)
    else:
        # If user didn't send number by button
        bot.send_message(user_id, 'Please send your phone number by button!',
                         reply_markup=bt.num_bt())
        bot.register_next_step_handler(message, get_number, name)

# Step for add location
def get_location(message, name, number):
    user_id = message.from_user.id
    # If user sent location by button
    if message.location:
        location = str(geolocation.reverse(f'{message.location.latitude},'
                                           f'{message.location.longitude}'))
        db.register(user_id, name, number, location)
        bot.send_message(user_id, 'Amazing! Registration done!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        # If user didn't send location by button
        bot.send_message(user_id, 'Please send your location by button!',
                         reply_markup=bt.loc_bt())
        bot.register_next_step_handler(message, get_location, name)


bot.polling(non_stop=True)

