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
        products = db.get_pr_but()
        bot.send_message(user_id, f'Hello {message.from_user.first_name}\n!'
                                  'Welcome back to our Storm Store or short format SS',
                                  reply_markup=bt.main_memu_buttons(products))
    else:
        bot.send_message(user_id, f'Hello {message.from_user.first_name}!\n'
                         "Welcome to our Storm Store\n"
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
        products = db.get_pr_but()
        bot.send_message(user_id, 'Amazing! Registration done!',
                         reply_markup=bt.main_memu_buttons(products))
    else:
        # If user didn't send location by button
        bot.send_message(user_id, 'Please send your location by button!',
                         reply_markup=bt.loc_bt())
        bot.register_next_step_handler(message, get_location, name, number)


@bot.message_handler(commands=['admin'])
def act(message):
    admin_id = 5239314473
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Choice action!', reply_markup=bt.admin_menu())
        # Next step to choice
        bot.register_next_step_handler(message, admin_choice)
    else:
        bot.send_message(message.from_user.id, 'You are not admin!')

# Choice admin action
def admin_choice(message):
    admin_id = 5239314473
    if message.text == 'Add product':
        bot.send_message(admin_id, 'Text name of product',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_pr_name)
    elif message.text == 'Delete product':
        check = db.check_pr()
        if check:
            bot.send_message(admin_id, 'Text id of product',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_pr_id)
        else:
            bot.send_message(admin_id, 'Product not exist in base yet!')
            bot.register_next_step_handler(message, admin_choice)
    elif message.text == 'Change product':
        check = db.check_pr()
        if check:
            bot.send_message(admin_id, 'Text id of product',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_pr_change)
        else:
            bot.send_message(admin_id, 'Product not exist in base yet!',)
            bot.register_next_step_handler(message, admin_choice)
    elif message.text == 'Go to menu':
        products = db.get_pr_but()
        bot.send_message(admin_id, 'Welcome to menu!',
                         reply_markup=bt.main_memu_buttons(products))
    else:
        bot.send_message(admin_id, 'Unknown command!', reply_markup=bt.admin_menu())
        bot.register_next_step_handler(message, admin_choice)

# Step to take name odf product
def get_pr_name(message):
    admin_id = 5239314473
    if message.text:
        pr_name = message.text
        bot.send_message(admin_id, 'Great! Now make description!')
        # Step to take description
        bot.register_next_step_handler(message, get_pr_des, pr_name)
    else:
        bot.send_message(admin_id, 'Send name of product by text format!')
        bot.register_next_step_handler(message, get_pr_name)

# Step for make description for product
def get_pr_des(message, pr_name):
    admin_id = 5239314473
    if message.text:
        pr_des = message.text
        bot.send_message(admin_id, 'Now enter the count of product')
        # Step to get count for product
        bot.register_next_step_handler(message, get_pr_count, pr_name, pr_des)
    else:
        bot.send_message(admin_id, 'Send description of product by text format!')
        bot.register_next_step_handler(message, get_pr_des, pr_name)

# Step to take count of product
def get_pr_count(message, pr_name, pr_des):
    admin_id = 5239314473
    try:
        pr_count = int(message.text)
        bot.send_message(admin_id, 'Now go to site https://postimages.org/ru/, and upload photo of product'
                                   ' and send link to it')
        # Step to get photo for product
        bot.register_next_step_handler(message, get_pr_photo, pr_name, pr_des, pr_count)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Send count of product in whole number and positive format!')
        #  Return to the function
        bot.register_next_step_handler(message, get_pr_count, pr_name, pr_des)

# Step to take a photo for product
def get_pr_photo(message, pr_name, pr_des, pr_count):
    admin_id = 5239314473
    if message.text:
        pr_photo = message.text
        bot.send_message(admin_id, 'Great! Now what cost of product?')
        # Step to take to photo
        bot.register_next_step_handler(message, get_pr_cost, pr_name, pr_des, pr_count, pr_photo)
    else:
        bot.send_message(admin_id, 'Incorrect format link!')
        bot.register_next_step_handler(message, get_pr_photo, pr_name, pr_des, pr_count)

# Step to take cost
def get_pr_cost(message, pr_name, pr_des, pr_count, pr_photo):
    admin_id = 5239314473
    try:
        pr_price = float(message.text)
        db.add_pr(pr_name, pr_des, pr_count, pr_photo, pr_price)
        bot.send_message(admin_id, 'Product added, want something else?', reply_markup=bt.admin_menu())
        bot.register_next_step_handler(message, admin_choice)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Send price in positive format!')
        #  Return to the function
        bot.register_next_step_handler(message, get_pr_cost, pr_name, pr_des, pr_count, pr_photo)

# Step to get product by id
def get_pr_id(message):
    admin_id = 5239314473
    try:
        pr_id = int(message.text)
        check = db.check_pr_id(pr_id)
        if check:
            db.del_pr(pr_id)
            bot.send_message(admin_id, 'Product deleted! Wanna something else?', reply_markup=bt.admin_menu())
            # Step to choice
            bot.register_next_step_handler(message, admin_choice)
        else:
            bot.send_message(admin_id, 'This product not exist in base!')
            # Return to function
            bot.register_next_step_handler(message, get_pr_id)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Something wrong with id\n'
                                   'Try again!')
        #  Return to the function
        bot.register_next_step_handler(message, get_pr_id)

# Step change count of product
def get_pr_change(message):
    admin_id = 5239314473
    try:
        pr_id = int(message.text)
        check = db.check_pr_id(pr_id)
        if check:
            bot.send_message(admin_id, 'How many products came?', reply_markup=bt.admin_menu())
            # Step "how many came"
            bot.register_next_step_handler(message, get_amount, pr_id)
        else:
            bot.send_message(admin_id, 'This product not exist in base!')
            # Return to function
            bot.register_next_step_handler(message, get_pr_change)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Something wrong with id\n'
                                   'Try again!')
        #  Return to the function
        bot.register_next_step_handler(message, get_pr_change)

# Step to "how many came?"
def get_amount(message, pr_id):
    admin_id = 5239314473
    try:
        new_amount = int(message.text)
        db.change_pr_count(pr_id, new_amount)
        bot.send_message(admin_id, 'Count of product changed! Wanna something else?')
        bot.register_next_step_handler(message, admin_choice)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Send count of product in whole number and positive format!')
        #  Return to the function
        bot.register_next_step_handler(message, get_amount, pr_id)


# Start product
bot.polling(non_stop=True)



