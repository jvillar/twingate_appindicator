# Linux Twingate App Indicator 

## Description
This repository hosts a Twingate App Indicator Linux systems using Gnome shell. It places an indicator in the notification area, allowing users to easily connect and disconnect from Twingate, as well as view the current connection status.

## Prerequisites
For Ubuntu 23.10 based systems, please install the following package before installing the App Indicator:
```sh
sudo apt-get install gir1.2-ayatanaappindicator3-0.1
```

## Installation

Clone or download this repository to your local machine:
   ```sh
   git clone https://github.com/jvillar/twingate_appindicator.git
   ```


##  Autostart
To have the Twingate app indicator start automatically with GNOME shell, configure it in GNOME's startup applications with the command `twingate_indicator.py` located at the root of the cloned repository.

## Usage
- **Connect**: Click on the notification area icon and select "Connect".
- **Disconnect**: Click on the icon and select "Disconnect".
- **View Status**: The icon will change or display a tooltip indicating the current connection status.

## Support
For any issues or questions, please open an issue on the GitHub repository.


