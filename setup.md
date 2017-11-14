# setting up opentoni

0. setup i2c, SPI, sounf = AUTO
     sudo raspi-config
    
1. install python dev
    
    sudo apt-get install python-dev


2. install SSD1306 Library for small oled display
    url: https://webnist.de/i2c-oled-display-mit-python-am-raspberrypi/
    github repo: https://github.com/adafruit/Adafruit_Python_SSD1306/tree/master/examples
    git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
    cd Adafruit_Python_SSD1306
    sudo python setup.py install

3. install Pillow
    sudo apt-get install python-pil


4. install rfid Library
    url: https://tutorials-raspberrypi.de/raspberry-pi-rfid-rc522-tueroeffner-nfc/

    4.1. install spi Library
        git clone https://github.com/lthiery/SPI-Py.git
        cd SPI-Py
        sudo python setup.py install
        cd ..

    4.2. RFID 522 Library
        git clone https://github.com/mxgxw/MFRC522-python.git 
        cd MFRC522-python
        test: sudo python Read.py

