import pygame, time, glob, random, os, keyboard, logging
from random import randrange, sample
from collections import defaultdict
from os.path import expanduser
home = os.path.expanduser('~pi')

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename=home+'/Raspberry-Pi-Audiomixer/Log.log', level=logging.DEBUG)

def loadMusicStyles():
	#Reads the musicstyleorder config file and assigns the read folders to numbers (1 to 9).
	logging.info('Loading music styles...')
	with open(home+'/Raspberry-Pi-Audiomixer/musicstyleorder') as file:
		musicstyledict = {}
		counter = 1
		for line in file:
			if line[0] != "#":
				line = line.replace("\n", "")
				logging.info('Recognized style: %s', line)
				musicstyledict[str(counter)] = line
				counter += 1
	return musicstyledict

musicstyledict = loadMusicStyles()
maxmusicvolume = 0.5
breaker = True
currentmusicstyle = "0"

#The following sets up the music channels.
logging.info('Initializing mixer...')
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.mixer.init()
warnsound = pygame.mixer.Sound(home+"/Raspberry-Pi-Audiomixer/sound/warning.wav")
secondsilence = pygame.mixer.Sound(home+"/Raspberry-Pi-Audiomixer/sound/silence-1-second.wav")
currentmusicchannel = "x"
logging.info('Prepping channel A...')
MusicChannelA = pygame.mixer.Channel(0)
MusicChannelA.play(secondsilence)
logging.info('Prepping channel B...')
MusicChannelB = pygame.mixer.Channel(1)
MusicChannelB.play(secondsilence)
currentplaylist = []
sfxdict = defaultdict(list)

def getRandomPlaylistOf(directory):
	#Searches for all music in the bgm subfolder in the music-style-folder that this is called with.
	#Then creates a randomized playlist out of all found music in that folder and returns that playlist.
	logging.info('Getting a random playlist for: %s', directory)
	finaldir = home+"/Raspberry-Pi-Audiomixer/sound/" + directory + "/bgm/*"
	logging.info(finaldir)
	playlist = []
	for result in glob.iglob(finaldir):
		playlist.insert(randrange(len(playlist)+1), result)
	logging.info('Done')
	return playlist

def getNextSongFromPlaylist():
	#Gets the next song in the playlist, removes it from the playlist and returns it.
	global currentplaylist
	logging.info('Returning next song in playlist: %s', currentplaylist[0])
	chosentitle = pygame.mixer.Sound(currentplaylist[0])
	currentplaylist.remove(currentplaylist[0])
	logging.info('Done')
	return chosentitle

def fadeTo(newdirection):
	#This loads the currently unused music channel with a new style (determined by the parameter string number) and fades from the current channel to the new one.
	global currentplaylist
	global currentmusicchannel
	global MusicChannelA
	global MusicChannelB
	global currentmusicstyle
	logging.info('Fading to a new style %s', newdirection)

	if currentmusicchannel == "x":
		currentmusicchannel = "a"

	logging.info('Loading new soundeffects')
	loadSoundEffects(musicstyledict[newdirection])
	logging.info('Loading new music')
	currentplaylist = getRandomPlaylistOf(musicstyledict[newdirection])
	logging.info('Begining fade...')
	
	if currentmusicchannel == "a":
		logging.info('Fading from A to B')
		currentmusicchannel = "b"
		vola = maxmusicvolume
		volb = 0
		MusicChannelB.play(getNextSongFromPlaylist())
		MusicChannelB.pause()
		MusicChannelB.unpause()
		while vola > 0:
			vola -= 0.01
			volb += 0.01
			MusicChannelA.set_volume(vola)
			MusicChannelB.set_volume(volb)
			time.sleep(0.03)
		logging.info('Done with fading')
		MusicChannelB.set_volume(maxmusicvolume)
		MusicChannelA.set_volume(0)
		checkTheQueue()
	else:
		logging.info('Fading from B to A')
		currentmusicchannel = "a"
		volb = maxmusicvolume
		vola = 0
		MusicChannelA.play(getNextSongFromPlaylist())
		MusicChannelA.pause()
		MusicChannelA.unpause()
		while volb > 0:
			volb -= 0.01
			vola += 0.01
			MusicChannelB.set_volume(volb)
			MusicChannelA.set_volume(vola)
			time.sleep(0.05)
		logging.info('Done with fading')
		MusicChannelA.set_volume(maxmusicvolume)
		MusicChannelB.set_volume(0)
		checkTheQueue()
	logging.info('Setting to a new directory')
	currentmusicstyle = newdirection
	logging.info('All done with the fading')

def loadSoundEffects(directory):
	#Loads new soundeffects into the public sfx dictionary
	global sfxdict
	logging.info('Loading soundeffects')
	sfxdict = defaultdict(list)
	finaldir = home+"/Raspberry-Pi-Audiomixer/sound/" + directory + "/sfx/"
	for item in glob.iglob(finaldir + "*"):
		item = item.replace(finaldir, "")
		sfxdict[item[0]].append(item)
	logging.info('Done loading soundeffects')

def checkTheQueue():
	#This will check if a song is queued after the current song. If not it will load one and queue it.
	global currentplaylist
	global currentmusicstyle
	if currentmusicchannel == "a":
		if MusicChannelA.get_queue() is None:
			logging.info('Nothing in the queue of A')
			if len(currentplaylist) == 0:
				logging.info('Playist empty, making a new one')
				currentplaylist = getRandomPlaylistOf(musicstyledict[currentmusicstyle])
			logging.info('Setting a new song')
			MusicChannelA.queue(getNextSongFromPlaylist())
	elif currentmusicchannel == "b":
		if MusicChannelB.get_queue() is None:
			logging.info('Nothing in the queue of B')
			if len(currentplaylist) == 0:
				logging.info('Playlist empty, making new one')
				currentplaylist = getRandomPlaylistOf(musicstyledict[currentmusicstyle])
			logging.info('Setting a new song')
			MusicChannelB.queue(getNextSongFromPlaylist())

def playByKey(key):
	#Takes in a keyboard key and tries to play a randomized sound from that keys loaded sfx
	logging.info('%s was pressed...', key)
	global sfxdict
	global musicstyledict
	global currentmusicstyle
	if currentmusicstyle != "0":
		if key in sfxdict:
			sfxToPlay = home+"/Raspberry-Pi-Audiomixer/sound/" + musicstyledict[currentmusicstyle] + "/sfx/" + random.choice(sfxdict[key])
			logging.info('Playing %s', sfxToPlay)
			pygame.mixer.Sound(sfxToPlay).play()
		else:
			pygame.mixer.Sound(warnsound).play()
			logging.info('No sfx loaded for %s', key)
	else:
		pygame.mixer.Sound(warnsound).play()
		logging.info('No music playing yet, no soundeffects for you!')
		
def turnMusicUp():
	#Raises the volume of the currently playing music channel by 0.1 up to a maximum of 1.0
	logging.info('Volume up...')
	fadeinprogress = True
	global maxmusicvolume
	global currentmusicchannel
	global MusicChannelA
	global MusicChannelB
	if maxmusicvolume < 0.99:
		vol = maxmusicvolume
		maxmusicvolume += 0.1		
		if currentmusicchannel == "a":
			while vol < maxmusicvolume:
				logging.info(vol)
				vol += 0.01
				MusicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol < maxmusicvolume:
				logging.info(vol)
				vol += 0.01
				MusicChannelB.set_volume(vol)
				time.sleep(0.03)
		MusicChannelA.set_volume(maxmusicvolume)
	else:
		logging.info('Volume is already at 100%')
	fadeinprogress = False
		
def turnMusicDown():
	#Lowers the volume of the currently playing music channel by 0.1 down to minimum of 0.0
	logging.info('Volume down...')
	fadeinprogress = True
	global maxmusicvolume
	global currentmusicchannel
	global MusicChannelA
	global MusicChannelB
	if maxmusicvolume > 0.01:
		vol = maxmusicvolume
		maxmusicvolume -= 0.1		
		if currentmusicchannel == "a":
			while vol > maxmusicvolume:
				logging.info(vol)
				vol -= 0.01
				MusicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol > maxmusicvolume:
				logging.info(vol)
				vol -= 0.01
				MusicChannelB.set_volume(vol)
				time.sleep(0.03)
		logging.info('Setting Volume at the end')
		MusicChannelA.set_volume(maxmusicvolume)
	else:
		logging.info('Volume is already at 0%')
	fadeinprogress = False

#Playing a startup sound to signal machine readiness.
logging.info('Playing startup sound')
pygame.mixer.Sound(home+'/Raspberry-Pi-Audiomixer/sound/startup-sound.wav').play()
logging.info('Entering loop...')
while breaker:
	checkTheQueue()
	if keyboard.is_pressed('space'):
		while keyboard.is_pressed('space'):
			pass
		logging.info('Space was pressed, waiting for a number to fade to a new music style...')
		while True:
			checkTheQueue()
			if keyboard.is_pressed('1') and '1' in musicstyledict:
				while keyboard.is_pressed('1'):
					pass
				fadeTo('1')
				break
			if keyboard.is_pressed('2') and '2' in musicstyledict:
				while keyboard.is_pressed('2'):
					pass
				fadeTo('2')
				break
			if keyboard.is_pressed('3') and '3' in musicstyledict:
				while keyboard.is_pressed('3'):
					pass
				fadeTo('3')
				break
			if keyboard.is_pressed('4') and '4' in musicstyledict:
				while keyboard.is_pressed('4'):
					pass
				fadeTo('4')
				break
			if keyboard.is_pressed('5') and '5' in musicstyledict:
				while keyboard.is_pressed('5'):
					pass
				fadeTo('5')
				break
			if keyboard.is_pressed('6') and '6' in musicstyledict:
				while keyboard.is_pressed('6'):
					pass
				fadeTo('6')
				break
			if keyboard.is_pressed('7') and '7' in musicstyledict:
				while keyboard.is_pressed('7'):
					pass
				fadeTo('7')
				break
			if keyboard.is_pressed('8') and '8' in musicstyledict:
				while keyboard.is_pressed('8'):
					pass
				fadeTo('8')
				break
			if keyboard.is_pressed('9') and '9' in musicstyledict:
				while keyboard.is_pressed('9'):
					pass
				fadeTo('9')
				break
			if keyboard.is_pressed('0') and '0' in musicstyledict:
				while keyboard.is_pressed('0'):
					pass
				fadeTo('0')
				break		
			if keyboard.is_pressed('space'):
				while keyboard.is_pressed('space'):
					pass
				logging.info('Fade aborted.')
				break
	if keyboard.is_pressed('1'):
		while keyboard.is_pressed('1'):
			pass
		playByKey('1')
	if keyboard.is_pressed('2'):
		while keyboard.is_pressed('2'):
			pass
		playByKey('2')
	if keyboard.is_pressed('3'):
		while keyboard.is_pressed('3'):
			pass
		playByKey('3')
	if keyboard.is_pressed('4'):
		while keyboard.is_pressed('4'):
			pass
		playByKey('4')
	if keyboard.is_pressed('5'):
		while keyboard.is_pressed('5'):
			pass
		playByKey('5')
	if keyboard.is_pressed('6'):
		while keyboard.is_pressed('6'):
			pass
		playByKey('6')
	if keyboard.is_pressed('7'):
		while keyboard.is_pressed('7'):
			pass
		playByKey('7')
	if keyboard.is_pressed('8'):
		while keyboard.is_pressed('8'):
			pass
		playByKey('8')
	if keyboard.is_pressed('9'):
		while keyboard.is_pressed('9'):
			pass
		playByKey('9')
	if keyboard.is_pressed('0'):
		while keyboard.is_pressed('0'):
			pass
		playByKey('0')
	if keyboard.is_pressed('+'):
		while keyboard.is_pressed('+'):
			pass
		turnMusicUp()
	if keyboard.is_pressed('-'):
		while keyboard.is_pressed('-'):
			pass
		turnMusicDown()
	if keyboard.is_pressed('enter'):
		while keyboard.is_pressed('enter'):
			pass
		rlybreak = True
		logging.info('Enter was pressed. Really quit? Press Enter again to quit, press something else to abort...')
		while rlybreak:
			if keyboard.is_pressed('enter'):
				logging.info('We are out then')
				breaker = False
				rlybreak = False
				break
			if keyboard.is_pressed('0'):
				while keyboard.is_pressed('0'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('1'):
				while keyboard.is_pressed('1'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('2'):
				while keyboard.is_pressed('2'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('3'):
				while keyboard.is_pressed('3'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('4'):
				while keyboard.is_pressed('4'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('5'):
				while keyboard.is_pressed('5'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('6'):
				while keyboard.is_pressed('6'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('7'):
				while keyboard.is_pressed('7'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('8'):
				while keyboard.is_pressed('8'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
				logging.info('Not quitting yet')
			if keyboard.is_pressed('9'):
				while keyboard.is_pressed('9'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
			if keyboard.is_pressed('space'):
				while keyboard.is_pressed('space'):
					pass
				logging.info('Not quitting yet')
				rlybreak = False
				break
	else:
		pass