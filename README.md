# Raspberry-Pi-Audiomixer
This little python script is my way of turning a Raspberry Pi into a mobile background-music machine with sound effects.
Intended to be used for board and role playing games. When ran it will start a pygame application and accept user input on the keyboard. The numbers (Keypad not supported yet) change the channel around and the letters are used to fire sound effects.

You will need to have installed:
wmctrl (this will be used to always shift the pygame window into the foreground)
python 2.7.6 (Well, duh)
pygame (This won't run otherwise)
python keyboard module (https://pypi.org/project/keyboard/ I had version 0.13.1 when coding this)

Nice to have:
ffmpeg or avconv (useful to wav any music and soundeffect you have. USE ONLY WAV FILES FOR SOUNDEFFECTS AND MUSIC!! If your Music or soundeffects don't play and only a faint crack is hearable, then you haven't converted them to wav correctly. usea different program!!"


Setup:
- Create Directories in the sound folder, create subdirectories in those named "bgm" (backgroundmusic) and "sfx" (soundeffects)
- Put music in wav format into the bgm folder, naming does not really matter. 
- Put sound effects in wav format into the sfx folder. Important: put a numeral in the front of the filename to map them to numeral keys (eg. "3_boing.wav" will map to the button 3 when the specific music style is loaded). You can map multiple soundeffects to a single numeral button, a random one will be played after hitting the key.
- Edit the musicstyleorder in the main directory and change according to the instructions inside

IMPORTANT:
The Script expects to be run as superuser and the main directory should be located in some users home dir.
Change the user on line 5 in the Main.py to that user, then run 'sudo python Main.py'

Useage:
After Startup you will hear a startup sound. Afterwards try pressing numeral buttons (1-0). An error sound should play, because no music style has been loaded yet.
Press space followed by the number of music style you want to switch to, determined in the musicstyleorder file.
Script should switch to the music style and play a random piece of music.
Now press numeral buttons to which you mapped soundeffects. A random one will play if you mapped more than one to a single numeral.

Hit Enter twice to abort script. 
