# Raspberry-Pi-Audiomixer
This little python script is my way of turning a Raspberry Pi into a mobile background-music machine with sound effects.
Intended to be used for board- and role playing games. When ran it will start a pygame application and accept user input on an attached keypad. By hitting space followed by a number, you will be able to change the music channel, which will load up individual soundeffects with it. The sfx can then be fired seperately by hitting the numbers loaded up with the sfx.

## You will need to have installed:
- python 2.7.6 (Well, duh)
- pygame (This won't run otherwise)
- python keyboard module (https://pypi.org/project/keyboard/ I had version 0.13.1 when coding this)

### Nice to have:
- ffmpeg or avconv (useful to wav any music and soundeffect you have. USE ONLY WAV FILES FOR SOUNDEFFECTS AND MUSIC!! If your Music or soundeffects don't play and only a faint crack is hearable, then you haven't converted them to wav correctly. usea different program!!"


## Setup:
- Clone this directory to your raspberry pi, into the homedirectory of a user (This was tested and developed on a raspberry pi B, with Raspbian)
- Install all required programs on the pi
- Create Directories in the sound folder, create subdirectories in those named "bgm" (backgroundmusic) and "sfx" (soundeffects) (See examples already included)
- Put music in wav format into the bgm folder, naming does not really matter. 
- Put sound effects in wav format into the sfx folder. It's important here to put a numeral in the front of the filename to map them to numeral keys (eg. "3_boing.wav" will map to the button 3 when the specific music style is loaded). You can map multiple soundeffects to a single numeral button, a random one will be played after hitting the key.
- Edit the musicstyleorder in the main directory and change according to the instructions inside
- Change the user on line 5 in the Main.py to the username where the main Folder of the Audiomixer is located
- Run 'sudo python Main.py'

Alternatively put it into your /etc/rc.local (eg. 'sudo python /home/pi/Raspberry-Pi-Audiomixer/Main.py') so it boots up on startup. You can hear the startup.wav for verification that the program started.

## Useage:
- After Startup you will hear a startup sound. Afterwards try pressing numeral buttons (1-0). An error sound should play, because no music style has been loaded yet.
- Press space followed by the number of music style you want to switch to, determined in the musicstyleorder file.
- Script should switch to the music style and start playing a random piece of music from that style.
- Now press numeral buttons to which you mapped soundeffects. A random one will play if you mapped more than one to a single numeral.
- Hit Enter twice to abort script. 

## Currently working Keys:
- Space, which enters the program into a state in which you can change the music style.
- Numbers (1234567890), which will either play a sfx that was specified for that key, or load a new music style if space was pressed beforehand.
- Plus and Minus, which will turn up and down the volume of the music.
- Enter, which, if hit twice, will exit the program.

## Other Stuff:
- Examplemusic by https://www.bensound.com .Check it out!
- Examplesfx are by yours truly. Use as you wish.
- The Examples enclosed are in mp3 format, because it's smaller. But your pi is most likely not fast enough to decode mp3 in an acceptable length of time. So use the "convert_example_files.sh" to convert the files to wav, with avconv installed.