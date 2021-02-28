#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import pyautogui as pyautogui
import telebot
import os
from dotenv import load_dotenv


class BColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


class Command:
    LOCK = u'🔒'  # TODO
    UNLOCK = u'🔓'  # TODO
    LOCATION = u'🌍'  # TODO
    SCREENSHOT = u'🖼'  # TODO
    WEBCAM = u'📸'  # TODO
    POWER = u'🛑'  # TODO
    SUSPEND = u'🌙'  # TODO
    VOLUME_UP = u'🔊'  # TODO
    VOLUME_DOWN = u'🔉'  # TODO
    VOLUME_MUTE = u'🔇'  # TODO
    PLAY_PAUSE = u'⏯'  # TODO
    NEXT = u'⏭'  # TODO
    PREVIOUS = u'⏮'  # TODO
    INFO = u'ℹ️'  # TODO


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


if __name__ == '__main__':
    ascii()
    here_api, tl_token, tl_user_id = get_environment()
    tl_user_id = int(tl_user_id)
    bot = telebot.TeleBot(tl_token)


    def authorization(message):
        if message.chat.id != tl_user_id:
            bot.send_message(message.chat.id, "Unauthorized!!")
            return False
        return True

    print(BColors.GREEN + "[✓] Started.\n" + BColors.ENDC)
    print(BColors.YELLOW + "Waiting for Telegram commands\n" + BColors.ENDC)
    bot.polling(none_stop=True, interval=0, timeout=200)
