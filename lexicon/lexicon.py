LEXICON: dict[str, str] = {
    "/start": 'This bot was created for educational purposes and is a template with examples of using various functionality of the aiogram 3 framework for creating telegram bots. 🌿\n\n❓ Bot capabilities - /help\n\n🔗 Source: <a href="https://github.com/BLazzeD21/py-aiogram-template-bot">LINK</a>',
    "other": "This action does nothing",
    "admin": "admin",
    "main_menu_button": "Main menu 🧨",
    "profile_button": "Profile 🗃",
    "registration_button": "Registration 🖋",
    "cancel_button": "Cancel ❌",
    "info": "Information about the functionality of the bot:",
    "main": "🌫 Select an action: ",
    "main_kb_placeholder": "Choose an action...",
    "admin": "You're an admin",
    "click": "Click on the button:",
    "github": "Github repository",
    "aiogram": "Aiogram documentation",
    "back": "Come back ◀️",
    "back_profiles": "Come back ◀️",
    "nothing_to_cancel": "There is nothing to cancel. You are outside the state machine.\n\nTo return to registration - /registration",
    "cancel": "You have exited the state machine.\n\nTo return to registration - /registration",
    "registering": "You are registering.\n\nTo stop filling out the form, enter - /cancel",
    "enter_name": "Enter your name:",
    "incorrect_name": "You entered an incorrect name. Try again\n\nTo stop filling out the form, enter - /cancel",
    "enter_age": "Thank you!\n\nNow enter your age:",
    "incorrect_age": "You entered an incorrect age. Age must be a number between 1 and 100. Try again\n\nTo stop filling out the form, enter - /cancel",
    "enter_sex": "Thank you!\n\nChoose your gender:",
    "incorrect_gender": "Select gender using buttons. Try again\n\nTo stop filling out the form, enter - /cancel",
    "send_photo": "Thank you!\n\nSend your photo:",
    "incorrect_photo": "Send your photo\n\nTo stop filling out the form, enter - /cancel",
    "form_completed": "✅ You have exited the FSM.\nYou have successfully completed the form.\n\nThe profile can be viewed in the profile - /profile",
    "not_registered": "You have not registered. Registration - /registration",
    "enter_descr": "Enter your description:",
    "incorrect_descr": "You entered an incorrect description. Try again\n\nTo stop filling out the form, enter - /cancel",
    "select_account": "Select an account:",
    "backward": "<<",
    "forward": ">>",
}


def get_profile_data(user: dict, user_id: int):
    return f'Profile 🗂\n\n<b>ID:</b> <code>{user[user_id]["user_id"]}</code>\
    \n<b>Username:</b> @{user[user_id]["username"]}\
    \n<b>Name:</b> <code>{user[user_id]["name"]}</code>\
    \n<b>Age:</b> <code>{user[user_id]["age"]}</code>\
    \n<b>Sex:</b> <code>{user[user_id]["gender"]}</code>\
    \n<b>Description:</b> <code>{user[user_id]["description"]}</code>'


def get_help_commands(LEXICON_COMMANDS):
    help = "🤖 Available bot commands:\n\n"
    for key, value in LEXICON_COMMANDS.items():
        help += f"➖ {key} - {value}\n"
    return help
