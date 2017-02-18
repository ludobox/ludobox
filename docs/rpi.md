# Setup Ludobox on a Raspberry Pi

We need to :

- setup and run Raspian
- configure a Wifi access point  
- Install Ludobox software


# Setup Raspbian

Download [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) and copy to the pi

    sudo dd bs=4M if=2017-01-11-raspbian-jessie-lite.img of=/dev/mmcblk0
    sync


[Enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/) (add an `ssh` file to `/boot` disk )

    sudo touch /media/XXX/boot/ssh

Add wifi network

    sudo nano /media/XXX/etc/wpa_supplicant/wpa_supplicant.conf

Add your network info to `wpa_supplicant.conf`

    network={
    ssid="My WIFI"
    psk="mypassword"
    key_mgmt=WPA-PSK
    }

# Install the software

Check for your local IP on your router / define an alias

Connect to your pi

    ssh root@192.169.1.XX # your IP

Update everything

    sudo apt-get update && sudo apt-get upgrade

    sudo apt-get install build-essential git python-pip python-virtualenv python-dev


Config your pi

    raspi-config

Fix language issue

    export LANGUAGE=en_GB.UTF-8
    export LANG=en_GB.UTF-8
    export LC_ALL=en_GB.UTF-8
    locale-gen en_GB.UTF-8
    dpkg-reconfigure locales

Install

    git clone https://github.com/ludobox/ludobox
    cd ludobox
    python setup.py install



# Configure a WIFI access point (hotspot)

Follow those [intructions](https://cdn-learn.adafruit.com/downloads/pdf/setting-up-a-raspberry-pi-as-a-wifi-access-point.pdf)
see also [these](http://elinux.org/RPI-Wireless-Hotspot)  

Wifi [cards](https://www.raspberrypi.org/forums/viewtopic.php?f=36&t=76604)
R3 comes with a built-in hostspot
