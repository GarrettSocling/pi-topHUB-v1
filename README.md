# pi-topHUB v1

![Image of pi-topHUB v1 in a pi-top](
https://static.pi-top.com/images/v1-hub-pi-top.png "Image of pi-topHUB v1 in a pi-top")

![Image of pi-topHUB v1 in a pi-topCEED](
https://static.pi-top.com/images/v1-hub-pi-topceed.png "Image of pi-topHUB v1 in a pi-topCEED")

## Table of Contents
* [Quick Start](#quick-start)
* [Hardware](#hardware)
* [Software](#software)
    * [pi-topHUB v1 on pi-topOS](#software-pt-os)
    * [pi-topHUB v1 on Raspbian](#software-raspbian)
    * [How it works - 'under the hood'](#software-how-it-works)
* [Using pi-topHUB v1](#using)
    * [Using a custom Python script](#using-script)
* [Documentation & Support](#support)
    * [Links](#support-links)
    * [Troubleshooting](#support-troubleshooting)

## <a name="quick-start"></a> Quick Start
#### pi-topHUB v1 on pi-topOS
* Boot into pi-topOS Stretch
* Your pi-top hub should work out of the box - enjoy!

---

#### pi-topHUB v1 on Raspbian
* Run the following commands in the terminal (with an internet connection):

```
sudo apt update
sudo apt install pt-hub
```

Alternatively, if you wish to add support for *all* pi-top devices:

```
sudo apt update
sudo apt install pt-devices
```

* Voilà!

## <a name="hardware"></a> Hardware

Unlike pi-topHUB v2, which comes with an HDMI to I2S converter, extra software configuration is required for high quality audio via I2S (as used in pi-topPULSE and pi-topSPEAKER (v1).

The hub is responsible for managing the display and audio signals, as well as for communicating with the pi-top v1's battery manager, if relevant.

#### Resources used by the pi-topHUB v1

pi-topHUB v1 uses the following resources:

* GPIO pins 19, 21, 23 and 26 for SPI communication

Additionally, pi-top v1 (not pi-topCEED) also communicates with the battery:

* GPIO pins 3 and 5 for I2C communication with pi-top battery, via I2C address 0x0b

_Note: GPIO pins are references by their physical number_

#### Extra required configuration
##### Dependencies
* python3-pt-common
  * Common class of Python operations (see [this repository](https://github.com/pi-top/Device-Management))
* python3-smbus
  * Used to communicate via I2C with pi-top's battery
* python3-spidev
  * Used to communicate with pi-topHUB v1

## <a name="software"></a> Software
#### <a name="software-pt-os"></a> pi-topHUB v1 on pi-topOS

All pi-topHUB v1 software and libraries are included and configured 'out-of-the-box' as standard on pi-topOS Stretch (2018 onwards).

Download the latest version of pi-topOS [here](https://pi-top.com/products/os#download).

##### Technical information
Automatic initialisation is performed by the software contained in the package called `pt-device-manager`. This installs a program called `pt-device-manager`, which runs in the background and scans for newly connected devices. If a device is detected (and its supporing library is installed), it will be initialised and enabled automatically.

When the `pt-hub` package is installed, `pt-device-manager` will also be installed as dependency, thus starting the background process. The hub will be initialised and ready to use immediately.

`pt-device-manager` is also responsible for powering off the Raspberry Pi when a pi-top device shuts down. More information on shutdown can be found [here](https://github.com/pi-top/Device-Management/poweroff).

For more information about pt-device-manager, see [this repository](https://github.com/pi-top/Device-Management).

#### <a name="software-raspbian"></a> pi-topHUB v1 on Raspbian
The pi-topHUB v1 software can be found on the Raspbian software repositories. To install it, simply run the following commands at the terminal and then reboot:


```
sudo apt update
sudo apt install pt-hub
```

This will install the pthub Python library, as well as its dependencies, including pt-device-manager (see above).

If you prefer to manually install, see the [Manual Configuration and Installation](https://github.com/pi-top/pi-topHUB-v1/blob/master/manual-install/manual-configuration.md) instructions.

#### <a name="software-how-it-works"></a> How it works - 'under the hood'
For more information on how to use the library files, check out the [examples](https://github.com/pi-top/pi-topHUB-v1/tree/master/examples) folder for guidance of what the library is capable of.

## <a name="using"></a> Using pi-topHUB v1

#### <a name="using-script"></a> Using a custom Python script

Once installed, pi-topHUB v1 can be used in Python3 by importing the `pthub` module in the `pthub` library.

Note that using the `pthub` Python module requires root access to function. If you are running a script, make sure that you are running it with root access. You can do this with the "sudo" command:

    sudo python3 my_cool_hub_script.py

Alternatively, if you are running Python in `IDLE`, please make sure you start LXTerminal and run idle or idle3 with the "sudo" command, like so:

    sudo idle3

## <a name="support"></a> Documentation & Support
#### <a name="support-links"></a> Links
* [Device Management (pt-device-manager)](https://github.com/pi-top/Device-Management)
* [Support](https://support.pi-top.com/)

#### <a name="support-troubleshooting"></a> Troubleshooting
#### Why is my pi-topHUB v1 not working?

There are a few possible reasons why it may not be working. If you are on pi-topOS, please run:

    pt-diagnostics

in the terminal on pi-topOS, and send the logs to pi-top support. This will ensure that we can provide you with the best information to help fix the issue.

If you get `No such file or directory`, run the following:

    sudo apt install pt-diagnostics
    pt-diagnostics

#### Why is my pi-top v1 reporting itself to be a pi-topCEED?

`pt-device-manager` uses the presence of the battery to identify a pi-top v1.
If this is not possible, then it will assume that it is now connected to a pi-topCEED.
The battery is detected by scanning for its I2C address (0x0b). You can see if the Raspberry Pi can 'see' the device by scanning for I2C addresses:

    sudo i2cdetect -y 1

If you cannot see `0b` in the list, then there is likely a hardware fault. This might be a problem with the Raspberry Pi or the hub. Please follow the instructions under `Why is my pi-topHUB v1 not working?` for assistance with this.