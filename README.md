# :computer: TyRemote
![Python3](https://img.shields.io/badge/language-Python3-blue) ![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-green)

TyRemote (**T**elegram + P**y**thon + **Remote**) is a remote control tool for laptops.
It allows you to control your PC with a Telegram Bot. You can:
* shut down
* sleep :zzz:
* get location :pushpin:
* controls the multimedia (volume, play, pause, ...) :musical_note:
* take webcam photo :camera:
* take a screenshot :computer:
* lock/unlock :unlock:
* and check your PC status

It is compatible with Windows and Linux. Note that I built this program for personal purposes, may not be compatible with all Linux distributions. See later the [VirtualPC section.](#virtualpc)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Clone this repository and run this command to install all dependencies

```
$ pipenv install --ignore-pipfile
```

It requires that on Linux you have "iwlist", "iw" and "awk" installed. And on Windows "WifiInfoView.exe" (see below). 

Besides, it is required to have installed the dependencies related to the implementation of [VirtualPC](#virtualpc).

### Installing
First, you create a new Here API key by following these [steps](https://developer.here.com/documentation/identity-access-management/dev_guide/topics/plat-using-apikeys.html).

Next, create a new `.env` file with the format:
```ini
TYR_HERE_API_KEY=<YOUR_HERE_NETWORK_POSITION_API_KEY>
TYR_TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
TYR_TELEGRAM_USER_ID=<YOUR_TELEGRAM_USER_ID>
```
Last, you need to create a cron that runs the `TyRemote.py` script with administrator privileges when starting the laptop.


## TODOs
I want to add :thinking: the next functionalities to TyRemote:
- [ ] Full Windows compatibility
- [ ] Upload and download files from Laptop
- [ ] File system navigation
- [ ] Record a video from the webcam
- [ ] Run CLI commands


## Built With
TyRemote uses the next dependencies:
* pyTelegramBotAPI ([see here](https://github.com/eternnoir/pyTelegramBotAPI))
* python-dotenv
* requests
* pyautogui
* opencv-python
* psutil
* iwlist.py ([see here](https://github.com/iancoleman/python-iwlist)). It is included with the source code in this repository.

And it is built-in **Python 3**.


## About
### Telegram Bot
TyRemote requires a Telegram Bot to works. You can create one by following the [steps below](https://core.telegram.org/bots#6-botfather). Further, it is necessary to know your
Telegram chat' id, for this you can use bot @getmyid_bot.

### Localization
To locate your laptop TyRemote uses the Wi-Fi networks and/or the public IP. It first scans all nearby networks and sends this to the [HERE Network Positioning API v1](https://developer.here.com/documentation/positioning/dev_guide/topics/request-first-locate.html) to get an approximate location. If it fails, locates the PC using [ip-api](https://ip-api.com/). 

**Note:** In Linux the program uses **iwlist** that require **root** permissions.

### VirtualPC
For some commands like shutdown, their implementation is different on Windows and Linux. To facilitate its implementations, I created the VirtualPC class that defines the methods that you must implement to achieve compatibility with your system.
Currently, the program has an implementation for Xubuntu using:
* amixer to control volume
* xdotool to control multimedia
* systemctl to shutdown and sleep.


### WifiInfoView
In windows, to get Wi-Fi networks TyRemote uses WifiInfoView.exe. You can download it from [here](https://www.nirsoft.net/utils/wifi_information_view.html) and copy it.

## Contributing

I am not currently aiming to achieve a professional tool, this is only for simple uses, but this does not limit you to contribute by submitting pull requests for improvements and bug fixes.
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
It does not include the file `iwlist.py` of the [repository](https://github.com/iancoleman/python-iwlist) that does not specify a license.


