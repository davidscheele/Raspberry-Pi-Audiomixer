import pygame, time, glob, random, os, keyboard, logging
from random import randrange, sample
from collections import defaultdict
from os.path import expanduser
home = os.path.expanduser('~pi')

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename=home+'/Raspberry-Pi-Audiomixer/Log.log', level=logging.DEBUG)

breaker = True

currentMusicStyle = "0"

logging.info('')
def loadMusicStyles():	
	logging.info('Loading Music Styles')
	with open(home+'/Raspberry-Pi-Audiomixer/musicstyleorder') as file:
		musicStyleDict = {}
		counter = 1
		for line in file:
			if line[0] != "#":
				line = line.replace("\n", "")
				logging.info('Recognized style: %s', line)
				musicStyleDict[str(counter)] = line
				counter += 1
	return musicStyleDict

musicStyleDict = loadMusicStyles()
maxMusicVolume = 0.5

warnSound = home+"/Raspberry-Pi-Audiomixer/sound/warning.wav"
secondSilence = home+"/Raspberry-Pi-Audiomixer/sound/silence-1-second.wav"

logging.info('Preinit of mixer')
pygame.mixer.pre_init(22050, -16, 2, 512)
logging.info('Init Mixer')
pygame.mixer.init()
currentMusicChannel = "x"
logging.info('Prepping Channel A')
musicChannelA = pygame.mixer.Sound(secondSilence).play()
logging.info('Prepping Channel B')
musicChannelB = pygame.mixer.Sound(secondSilence).play()
currentPlaylist = []
sfxDict = defaultdict(list)

def getRandomPlaylistOf(directory):
	logging.info('Getting a Radom Playlist')
	finaldir = home+"/Raspberry-Pi-Audiomixer/sound/" + directory + "/bgm/*"
	logging.info(finaldir)
	playlist = []
	for result in glob.iglob(finaldir):
		playlist.insert(randrange(len(playlist)+1), result)
	logging.info('Done')
	return playlist

def getNextSongFromPlaylist():
	logging.info('Getting next song from playlist')
	global currentPlaylist
	logging.info(currentPlaylist[0])	
	chosenTitle = currentPlaylist[0]
	currentPlaylist.remove(currentPlaylist[0])
	logging.info('Done')
	return chosenTitle

def fadeTo(newDirection):
	logging.info('Fading to a new style...')
	global currentPlaylist
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	global currentMusicStyle

	if currentMusicChannel == "x":
		currentMusicChannel = "a"
	
	logging.info('Loading new Soundeffects...')
	loadSoundEffects(musicStyleDict[newDirection])
	logging.info('Getting new Music...')
	currentPlaylist = getRandomPlaylistOf(musicStyleDict[newDirection])
	
	logging.info('Begin Fading...')
	
	if currentMusicChannel == "a":
		logging.info('Fading from A')
		currentMusicChannel = "b"
		vola = maxMusicVolume
		volb = 0
		logging.info('Play and pause on B')
		musicChannelB = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		logging.info('Playing song on B')
		musicChannelB.pause()
		logging.info('Paused song on B')
		logging.info('Unpause song on B')
		musicChannelB.unpause()
		while vola > 0:
			logging.info('Fading...')
			vola -= 0.01
			volb += 0.01
			logging.info('Setting Volumes')
			musicChannelA.set_volume(vola)
			musicChannelB.set_volume(volb)
			time.sleep(0.03)
		logging.info('Done with fading.')
		checkTheQueue()
		musicChannelB.set_volume(maxMusicVolume)
	else:
		logging.info('Fading from B')
		currentMusicChannel = "a"
		volb = maxMusicVolume
		vola = 0
		logging.info('Play and pause on A')
		musicChannelA = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		logging.info('Playing song on A')
		musicChannelA.pause()
		logging.info('Paused song on A')
		logging.info('Unpause song on A')
		musicChannelA.unpause()
		while volb > 0:
			logging.info('Fading...')
			volb -= 0.01
			vola += 0.01
			logging.info('Setting Volumes')
			musicChannelB.set_volume(volb)
			musicChannelA.set_volume(vola)
			time.sleep(0.05)
		logging.info('Done with fading.')
		checkTheQueue()
		musicChannelA.set_volume(maxMusicVolume)
	logging.info('Setting the new directory as the current directory')
	currentMusicStyle = newDirection
	logging.info('All done with the fading')

def loadSoundEffects(directory):
	logging.info('Loading Soundeffects...')
	global sfxDict

	sfxDict = defaultdict(list)
	finaldir = home+"/Raspberry-Pi-Audiomixer/sound/" + directory + "/sfx/"
	for item in glob.iglob(finaldir + "*"):
		item = item.replace(finaldir, "")
		sfxDict[item[0]].append(item)
	logging.info('Done loading Soundeffects')

def checkTheQueue():
	global currentPlaylist
	global currentMusicStyle
	if currentMusicChannel == "a":
		if musicChannelA.get_queue() is None:
			logging.info('Nothing in the Queue of A')
			if len(currentPlaylist) == 0:
				logging.info('Playist empty, making a new one')
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			logging.info('Setting a new song')
			logging.info(currentPlaylist[0])	
			musicChannelA.queue(pygame.mixer.Sound(currentPlaylist[0]))
			logging.info('Removing from playlist')
			currentPlaylist.remove(currentPlaylist[0])
			logging.info('Done')
	elif currentMusicChannel == "b":
		if musicChannelB.get_queue() is None:
			logging.info('Nothing in the Queue of B')
			if len(currentPlaylist) == 0:
				logging.info('Playlist empty, making new one')
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			logging.info('Setting a new song')
			logging.info(currentPlaylist[0])
			musicChannelB.queue(pygame.mixer.Sound(currentPlaylist[0]))
			logging.info('Removing from playlist')
			currentPlaylist.remove(currentPlaylist[0])
			logging.info('Done')

def playByKey(key):
	logging.info('Playing something because %s %s', key, ' was pressed')
	global sfxDict
	global musicStyleDict
	global currentMusicStyle
	if currentMusicStyle != "0":
		if key in sfxDict:
			logging.info('I have a sound for that!!')
			sfxToPlay = home+"/Raspberry-Pi-Audiomixer/sound/" + musicStyleDict[currentMusicStyle] + "/sfx/" + random.choice(sfxDict[key])
			logging.info('Playing %s', sfxToPlay)
			pygame.mixer.Sound(sfxToPlay).play()
			logging.info('I played it, are ya happy?')
		else:
			pygame.mixer.Sound(warnSound).play()
			logging.info('I have nothing for %s', key)
	else:
		pygame.mixer.Sound(warnSound).play()
		logging.info('No music playing yet, no soundeffects for you!')
		
def turnMusicUp():
	logging.info('Turn the Volume up!')
	global maxMusicVolume
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	if maxMusicVolume < 0.99:
		vol = maxMusicVolume
		maxMusicVolume += 0.1		
		if currentMusicChannel == "a":
			while vol < maxMusicVolume:
				logging.info(vol)
				vol += 0.01
				musicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol < maxMusicVolume:
				logging.info(vol)
				vol += 0.01
				musicChannelB.set_volume(vol)
				time.sleep(0.03)
		logging.info('Setting the Volume at the end')
		musicChannelA.set_volume(maxMusicVolume)
	else:
		logging.info('Volume is already at 100%')
		
def turnMusicDown():
	logging.info('Turn the Volume down!')
	global maxMusicVolume
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	if maxMusicVolume > 0.01:
		vol = maxMusicVolume
		maxMusicVolume -= 0.1		
		if currentMusicChannel == "a":
			while vol > maxMusicVolume:
				logging.info(vol)
				vol -= 0.01
				musicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol > maxMusicVolume:
				logging.info(vol)
				vol -= 0.01
				musicChannelB.set_volume(vol)
				time.sleep(0.03)
		logging.info('Setting Volume at the end')
		musicChannelA.set_volume(maxMusicVolume)
	else:
		logging.info('Volume is already at 100%')

logging.info('Startup Sound')
pygame.mixer.Sound(home+'/Raspberry-Pi-Audiomixer/sound/startup-sound.wav').play()
logging.info('Entering while loop')
while breaker:
	checkTheQueue()
	if keyboard.is_pressed('space'):
		while keyboard.is_pressed('space'):
			pass
		logging.info('Space was pressed, waiting for a number to fade to a new music style...')
		while True:
			checkTheQueue()
			if keyboard.is_pressed('1') and '1' in musicStyleDict:
				while keyboard.is_pressed('1'):
					pass
				logging.info('1')
				fadeTo('1')
				break
			if keyboard.is_pressed('2') and '2' in musicStyleDict:
				while keyboard.is_pressed('2'):
					pass
				logging.info('2')
				fadeTo('2')
				break
			if keyboard.is_pressed('3') and '3' in musicStyleDict:
				while keyboard.is_pressed('3'):
					pass
				logging.info('3')
				fadeTo('3')
				break
			if keyboard.is_pressed('4') and '4' in musicStyleDict:
				while keyboard.is_pressed('4'):
					pass
				logging.info('4')
				fadeTo('4')
				break
			if keyboard.is_pressed('5') and '5' in musicStyleDict:
				while keyboard.is_pressed('5'):
					pass
				logging.info('5')
				fadeTo('5')
				break
			if keyboard.is_pressed('6') and '6' in musicStyleDict:
				while keyboard.is_pressed('6'):
					pass
				logging.info('6')
				fadeTo('6')
				break
			if keyboard.is_pressed('7') and '7' in musicStyleDict:
				while keyboard.is_pressed('7'):
					pass
				logging.info('7')
				fadeTo('7')
				break
			if keyboard.is_pressed('8') and '8' in musicStyleDict:
				while keyboard.is_pressed('8'):
					pass
				logging.info('8')
				fadeTo('8')
				break
			if keyboard.is_pressed('9') and '9' in musicStyleDict:
				while keyboard.is_pressed('9'):
					pass
				logging.info('9')
				fadeTo('9')
				break
			if keyboard.is_pressed('0') and '0' in musicStyleDict:
				while keyboard.is_pressed('0'):
					pass
				logging.info('0')
				fadeTo('0')
				break		
			if keyboard.is_pressed('space'):
				while keyboard.is_pressed('space'):
					pass
				logging.info('Alright, we are not fading then.')
				break
	if keyboard.is_pressed('1'):
		while keyboard.is_pressed('1'):
			pass
		logging.info('SFX key 1')
		playByKey('1')
	if keyboard.is_pressed('2'):
		while keyboard.is_pressed('2'):
			pass
		logging.info('SFX key 2')
		playByKey('2')
	if keyboard.is_pressed('3'):
		while keyboard.is_pressed('3'):
			pass
		logging.info('SFX key 3')
		playByKey('3')
	if keyboard.is_pressed('4'):
		while keyboard.is_pressed('4'):
			pass
		logging.info('SFX key 4')
		playByKey('4')
	if keyboard.is_pressed('5'):
		while keyboard.is_pressed('5'):
			pass
		logging.info('SFX key 5')
		playByKey('5')
	if keyboard.is_pressed('6'):
		while keyboard.is_pressed('6'):
			pass
		logging.info('SFX key 6')
		playByKey('6')
	if keyboard.is_pressed('7'):
		while keyboard.is_pressed('7'):
			pass
		logging.info('SFX key 7')
		playByKey('7')
	if keyboard.is_pressed('8'):
		while keyboard.is_pressed('8'):
			pass
		logging.info('SFX key 8')
		playByKey('8')
	if keyboard.is_pressed('9'):
		while keyboard.is_pressed('9'):
			pass
		logging.info('SFX key 9')
		playByKey('9')
	if keyboard.is_pressed('0'):
		while keyboard.is_pressed('0'):
			pass
		logging.info('SFX key 0')
		playByKey('0')
	if keyboard.is_pressed('+'):
		while keyboard.is_pressed('+'):
			pass
		logging.info('LOUDER')
		turnMusicUp()
	if keyboard.is_pressed('-'):
		while keyboard.is_pressed('-'):
			pass
		logging.info('Shut up a little?')
		turnMusicDown()
	if keyboard.is_pressed('enter'):
		while keyboard.is_pressed('enter'):
			pass
		rlybreak = True
		logging.info('Enter was pressed. Really quit? Press Enter again to quit')
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
	
