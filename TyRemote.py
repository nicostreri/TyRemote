#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform
import shutil
import socket
import os
import Localization
import VirtualPC
try:
    import psutil as psutil
    import pyautogui as pyautogui
    import telebot
    from dotenv import load_dotenv
    from telebot import types
    from requests import get
    import cv2
except ImportError:
    print("Some modules are not installed.")
    exit(1)

class BColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


class Command:
    LOCK = u'🔒 Lock'
    UNLOCK = u'🔓 Unlock'
    LOCATION = u'🌍'
    SCREENSHOT = u'🖼'
    WEBCAM = u'📸'
    POWER = u'🛑 Shutdown'
    SUSPEND = u'🌙 Sleep'
    VOLUME_UP = u'🔊'
    VOLUME_DOWN = u'🔉'
    VOLUME_MUTE = u'🔇'
    PLAY_PAUSE = u'⏯'
    NEXT = u'⏭'
    PREVIOUS = u'⏮'
    INFO = u'ℹ️'
    MANAGER = u'⚙ Manager'
    MULTIMEDIA = u'🎵 Media'
    MESSAGE = u'💬'
    GO_TO_MAIN = u'🔙 Exit'

def ascii():
    print(BColors.GREEN + " _____    ______                     _        " + BColors.ENDC)
    print(BColors.GREEN + "|_   _|   | ___ \                   | |       " + BColors.ENDC)
    print(BColors.GREEN + "  | |_   _| |_/ /___ _ __ ___   ___ | |_ ___  " + BColors.ENDC)
    print(BColors.GREEN + "  | | | | |    // _ \ '_ ` _ \ / _ \| __/ _ \ " + BColors.ENDC)
    print(BColors.GREEN + "  | | |_| | |\ \  __/ | | | | | (_) | ||  __/ " + BColors.ENDC)
    print(BColors.GREEN + "  \_/\__, \_| \_\___|_| |_| |_|\___/ \__\___| " + BColors.ENDC)
    print(BColors.GREEN + "      __/ |                                   " + BColors.ENDC)
    print(BColors.GREEN + "     |___/                                    " + BColors.ENDC)
    print(BColors.GREEN + "                                              " + BColors.ENDC)
    print(BColors.BLUE + "[-] Coded by Nicolás Streri (@nicostreri) [-]\n" + BColors.ENDC)


def __create_env_file():
    f_env = open(".env", "w")
    f_env.writelines([
        "TYR_HERE_API_KEY=\n",
        "TYR_TELEGRAM_BOT_TOKEN=\n",
        "TYR_TELEGRAM_USER_ID=\n"
    ])
    f_env.close()


def get_environment():
    load_dotenv()
    h_api = os.getenv("TYR_HERE_API_KEY")
    t_token = os.getenv("TYR_TELEGRAM_BOT_TOKEN")
    t_user_id = os.getenv("TYR_TELEGRAM_USER_ID")
    if h_api is None or t_token is None or t_user_id is None:
        print(BColors.RED + "[X] " + BColors.ENDC + "Complete the .env file\n")
        __create_env_file()
        exit(1)
    return h_api, t_token, t_user_id


def get_virtual_pc():
    instance = VirtualPC.get_virtual_pc_instance()
    if not instance.check_dependencies():
        print(BColors.RED + "[X] " + BColors.ENDC + "Dependencies required for virtual PC\n")
        exit(1)
    return instance


def check_binaries_dependencies():
    if shutil.which("iwlist") is None or shutil.which("iw") is None or shutil.which("awk") is None:
        print(BColors.RED + "[X] " + BColors.ENDC + "Dependencies required not installed (iwlist, iw, awk)\n")
        exit(1)


if __name__ == '__main__':
    ascii()
    here_api, tl_token, tl_user_id = get_environment()
    tl_user_id = int(tl_user_id)
    check_binaries_dependencies()
    bot = telebot.TeleBot(tl_token)
    pc = get_virtual_pc()

    def authorization(message):
        if message.chat.id != tl_user_id:
            bot.send_message(message.chat.id, "Unauthorized!!")
            return False
        return True


    def send_keyboard(tl_chat_id):
        markup = types.ReplyKeyboardMarkup()
        manager_btn = types.KeyboardButton(Command.MANAGER)
        multimedia_btn = types.KeyboardButton(Command.MULTIMEDIA)
        markup.row(manager_btn, multimedia_btn)
        bot.send_message(tl_chat_id, "Choose one option:", reply_markup=markup)


    def send_keyboard_manager(tl_chat_id):
        markup = types.ReplyKeyboardMarkup()
        power_btn = types.KeyboardButton(Command.POWER)
        suspend_btn = types.KeyboardButton(Command.SUSPEND)
        lock_btn = types.KeyboardButton(Command.LOCK)
        unlock_btn = types.KeyboardButton(Command.UNLOCK)
        info_btn = types.KeyboardButton(Command.INFO)
        location_btn = types.KeyboardButton(Command.LOCATION)
        screenshot_btn = types.KeyboardButton(Command.SCREENSHOT)
        webcam_btn = types.KeyboardButton(Command.WEBCAM)
        message_btn = types.KeyboardButton(Command.MESSAGE)
        back_btn = types.KeyboardButton(Command.GO_TO_MAIN)
        markup.row(power_btn, suspend_btn, info_btn)
        markup.row(location_btn, screenshot_btn, webcam_btn, message_btn)
        markup.row(lock_btn, unlock_btn)
        markup.row(back_btn)
        bot.send_message(tl_chat_id, "Choose one option:", reply_markup=markup)


    def send_keyboard_multimedia(tl_chat_id):
        markup = types.ReplyKeyboardMarkup()
        volume_up_btn = types.KeyboardButton(Command.VOLUME_UP)
        volume_down_btn = types.KeyboardButton(Command.VOLUME_DOWN)
        volume_mute_btn = types.KeyboardButton(Command.VOLUME_MUTE)
        play_pause_btn = types.KeyboardButton(Command.PLAY_PAUSE)
        next_btn = types.KeyboardButton(Command.NEXT)
        prev_btn = types.KeyboardButton(Command.PREVIOUS)
        back_btn = types.KeyboardButton(Command.GO_TO_MAIN)
        markup.row(volume_down_btn, volume_mute_btn, volume_up_btn)
        markup.row(prev_btn, play_pause_btn, next_btn)
        markup.row(back_btn)
        bot.send_message(tl_chat_id, "Choose one option:", reply_markup=markup)

    def virtual_pc_handler(func):
        def inner_function(*args, **kwargs):
            try:
                func(*args, **kwargs)
                bot.send_message(tl_user_id, "Executed!")
            except NotImplementedError:
                bot.send_message(tl_user_id, "Command not implemented!")

        return inner_function


    def send_system_status(tl_chat_id):
        text = ""
        text += "PC name: " + socket.gethostname()
        text += "\nOS: " + platform.system()
        text += "\nCPU: " + str(psutil.cpu_percent()) + "%"
        text += "\nMemory: " + str(int(psutil.virtual_memory().percent)) + "%"
        if psutil.sensors_battery():
            text += "\nBattery: " + str(format(psutil.sensors_battery().percent, ".0f")) + "%"
            if psutil.sensors_battery().power_plugged is True:
                text += " | Charging"
        text += "\nIP: " + get('http://ip-api.com/json/').json()["query"]
        bot.send_message(tl_chat_id, text)


    @bot.message_handler(commands=['location'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.LOCATION and authorization(msg))
    def localization_command(message):
        """
            Send the PC location
        """
        bot.send_chat_action(message.chat.id, "find_location")
        try:
            lat, lng = Localization.get_location_by_wifi()
            bot.send_message(message.chat.id, "By WiFi:")
            bot.send_location(message.chat.id, lat, lng)
        except Localization.FailedLocalization:
            try:
                lat, lng = Localization.get_location_by_ip()
                bot.send_message(message.chat.id, "By IP:")
                bot.send_location(message.chat.id, lat, lng)
            except Localization.FailedLocalization:
                bot.reply_to(message, "Could not get the location.")


    @bot.message_handler(commands=['screenshot'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.SCREENSHOT and authorization(msg))
    def screenshot_command(message):
        """
           Send a screenshot
        """
        try:
            image = pyautogui.screenshot()
            bot.send_chat_action(message.chat.id, "upload_photo")
            bot.send_photo(message.chat.id, image, timeout=100)
        except pyautogui.PyAutoGUIException:
            bot.reply_to(message, "Could not take screenshot")


    @bot.message_handler(commands=['webcam'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.WEBCAM and authorization(msg))
    def webcam_command(message):
        bot.send_chat_action(message.chat.id, 'upload_photo')
        camera = cv2.VideoCapture(0)
        _, image = camera.read()
        del camera
        _, encoded_image = cv2.imencode('.jpg', image)
        bot.send_photo(message.chat.id, encoded_image, timeout=100)


    @bot.message_handler(commands=['message'], func=authorization)
    def message_command(message):
        pyautogui.alert(message.text[9:])


    @bot.message_handler(commands=['info'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.INFO and authorization(msg))
    def info_command(message):
        send_system_status(message.chat.id)


    @bot.message_handler(commands=['lock'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.LOCK and authorization(msg))
    @virtual_pc_handler
    def lock_command(message):
        pc.lock()


    @bot.message_handler(commands=['unlock'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.UNLOCK and authorization(msg))
    @virtual_pc_handler
    def unlock_command(message):
        pc.unlock()


    @bot.message_handler(commands=['next'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.NEXT and authorization(msg))
    @virtual_pc_handler
    def next_command(message):
        pc.multimedia_next()


    @bot.message_handler(commands=['prev', 'previous'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.PREVIOUS and authorization(msg))
    @virtual_pc_handler
    def previous_command(message):
        pc.multimedia_prev()


    @bot.message_handler(commands=['play', 'pause'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.PLAY_PAUSE and authorization(msg))
    @virtual_pc_handler
    def play_pause_command(message):
        pc.multimedia_play_pause()


    @bot.message_handler(commands=['mute'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.VOLUME_MUTE and authorization(msg))
    @virtual_pc_handler
    def mute_command(message):
        pc.volume_mute()


    @bot.message_handler(commands=['volumeup'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.VOLUME_UP and authorization(msg))
    @virtual_pc_handler
    def volume_up_command(message):
        pc.volume_up()


    @bot.message_handler(commands=['volumedown'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.VOLUME_DOWN and authorization(msg))
    @virtual_pc_handler
    def volume_down_command(message):
        pc.volume_down()


    @bot.message_handler(commands=['poweroff'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.POWER and authorization(msg))
    @virtual_pc_handler
    def power_command(message):
        pc.shutdown()


    @bot.message_handler(commands=['suspend'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.SUSPEND and authorization(msg))
    @virtual_pc_handler
    def suspend_command(message):
        pc.sleep()


    @bot.message_handler(func=lambda msg: msg.text == Command.MESSAGE and authorization(msg))
    def send_message_command(message):
        bot.send_message(message.chat.id, "To display a message on the screen use:\n /message <text>")


    @bot.message_handler(commands=['start', 'help'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.GO_TO_MAIN and authorization(msg))
    def welcome_command(message):
        send_keyboard(message.chat.id)


    @bot.message_handler(commands=['manager'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.MANAGER and authorization(msg))
    def show_manager_commands_command(message):
        send_keyboard_manager(message.chat.id)


    @bot.message_handler(commands=['multimedia'], func=authorization)
    @bot.message_handler(func=lambda msg: msg.text == Command.MULTIMEDIA and authorization(msg))
    def show_multimedia_commands_command(message):
        send_keyboard_multimedia(message.chat.id)


    @bot.message_handler(func=authorization)
    def unknown_command(message):
        bot.reply_to(message, "What's you say?")
        send_keyboard(message.chat.id)

    print(BColors.GREEN + "[✓] Started.\n" + BColors.ENDC)
    bot.send_message(tl_user_id, "System started")
    send_system_status(tl_user_id)
    print(BColors.GREEN + "[✓] Startup report sent.\n" + BColors.ENDC)
    print(BColors.YELLOW + "Waiting for Telegram commands\n" + BColors.ENDC)
    bot.infinity_polling(timeout=200)
