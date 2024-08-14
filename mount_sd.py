# mount_sd.py will mount an SD card volume
import sys

import board, busio, sdcardio, storage, os
# setup pins for SPI
sck = board.GP10 # yellow
si = board.GP11 # blue
so = board.GP12 # green
cs = board.GP13 # yellow
spi = busio.SPI(sck, si, so)
sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
if 'sd' not in os.listdir('/'):
    print("***\nIMPORTANT: As of CircuitPython 9 you need to add a folder named 'sd' to your CIRCUITPY volume. \nPlease add a blank folder with this name so that your code will work properly.\n***")
    sys.exit()
storage.mount(vfs, "/sd")