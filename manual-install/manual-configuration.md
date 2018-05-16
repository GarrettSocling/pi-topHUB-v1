## Manually Configuring Raspbian for pi-topHUB v1

**Note:** This is definitely the long way round to get the pi-topHUB v1 working, and is provided only for interest. If you are running pi-topOS, you do not need to worry about this - everything is already included! If you are running Raspbian, please consult the `readme.md` file [here](https://github.com/pi-top/pi-topHUB-v1/blob/master/README.md) for the simpler method of configuring the hub.

### Enabling I2C (and SPI)

I2C is required to communicate with the function-enabling IC as part of initialisation.

The simplest way to do this is by running `raspi-config`, selecting `Interfacing Options` → `I2C` → Select "Yes" to enabling I2C.

### Making the `pthub2` Python library accessible

The easiest way to get the pi-topHUB v1 library is to install the Debian package directly:

    sudo apt install python3-pt-hub-v1

Note that this will only install the Python 3 library to communicate with the hub, and does not include the central device manager for plug-and-play functionality. If this is what you want, then install `pt-hub`:

	sudo apt install pt-hub

You can also download the library files from this repository and use them locally.

## Using the software library to manually initialise pi-topHUB v1

For more information on how to use the library files, check out the [examples](https://github.com/pi-top/pi-topHUB-v1/tree/master/examples) folder for guidance of what the library is capable of.

## Other useful stuff
### pt-hdmi-to-i2s

This is a script to configure enabling or disabling HDMI-to-I2S audio conversion on a pi-top V1, which is essential for some peripherals to work (such as pi-topPULSE/pi-topSPEAKER v1)

This is only needed for a manual setup.