#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform
import socket

import psutil as psutil
import pyautogui as pyautogui
import telebot
import os
from dotenv import load_dotenv
from requests import get

import Localization
import cv2


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


    print(BColors.GREEN + "[✓] Started.\n" + BColors.ENDC)
    print(BColors.YELLOW + "Waiting for Telegram commands\n" + BColors.ENDC)
    bot.polling(none_stop=True, interval=0, timeout=200)
