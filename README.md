# Raspberry-Pi-Audiomixer
This little python script is my way of turning a Raspberry Pi into a mobile background-music machine with sound effects.
Intended to be used for board and role playing games. When ran it will start a pygame application and accept user input on the keyboard. The numbers (Keypad not supported yet) change the channel around and the letters are used to fire sound effects.

You will need to have installed:
wmctrl (this will be used to always shift the pygame window into the foreground)
python 2.7.6 (Well, duh)
pygame (This won't run otherwise)
python keyboard module (https://pypi.org/project/keyboard/ I had version 0.13.1 when coding this)

Nice to have:
dir2ogg (Is nice to oggify whole directories. ONLY USE OGG FILES FOR MUSIC AND SOUNDEFFECTS!!)
