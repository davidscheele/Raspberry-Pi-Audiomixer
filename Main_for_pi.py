import pygame, time, glob, random, os, keyboard, logging
from random import randrange, sample
from collections import defaultdict

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='/home/pi/Raspberry-Pi-Audiomixer/Log.log', level=logging.DEBUG)

#os.environ["SDL_VIDEODRIVER"] = "dummy" # or maybe 'fbcon'

breaker = True

currentMusicStyle = "0"

logging.info('')
def loadMusicStyles():	
	logging.info('Loading Music Styles')
	with open('/home/pi/Raspberry-Pi-Audiomixer/musicstyleorder') as file:
		musicStyleDict = {}
		counter = 1
		for line in file:
			if line[0] != "#":
				line = line.replace("\n", "")
				logging.info('Recognized style: %s', line)
				musicStyleDict[str(counter)] = line
				counter += 1
#	print(musicStyleDict)
	return musicStyleDict

musicStyleDict = loadMusicStyles()
maxMusicVolume = 0.5

warnSound = "/home/pi/Raspberry-Pi-Audiomixer/warning.ogg"

logging.info('Init Pygame')
pygame.init()
logging.info('Init Mixer')
pygame.mixer.init()
logging.info('Init Display - Is this still needed?')
pygame.display.init()
logging.info('Init Screen - Is this still needed?')
SCREEN = pygame.display.set_mode((1, 1))
currentMusicChannel = "a"
logging.info('Prepping Channel A')
musicChannelA = pygame.mixer.Sound("/home/pi/Raspberry-Pi-Audiomixer/silence-1-second.wav").play()
logging.info('Prepping Channel B')
musicChannelB = pygame.mixer.Sound("/home/pi/Raspberry-Pi-Audiomixer/silence-1-second.wav").play()
currentPlaylist = []
sfxDict = defaultdict(list)

def getRandomPlaylistOf(directory):
	logging.info('Getting a Radom Playlist')
	finaldir = "/home/pi/Raspberry-Pi-Audiomixer/sound/" + directory + "/bgm/*"
	playlist = []
	for result in glob.iglob(finaldir):
		playlist.insert(randrange(len(playlist)+1), result)
	logging.info('Done')
	return playlist

def getNextSongFromPlaylist():
	logging.info('Getting next song from playlist')
	global currentPlaylist
	chosenTitle = currentPlaylist[0]
	currentPlaylist.remove(currentPlaylist[0])
	logging.info('Done')
	return chosenTitle

def fadeTo(newDirection):
	logging.info('Fading to a new style')
	global currentPlaylist
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	global currentMusicStyle
	
#	print("getting all the stuff")
	
	logging.info('Loading new Soundeffects')
	loadSoundEffects(musicStyleDict[newDirection])
	logging.info('Getting new Music')
	currentPlaylist = getRandomPlaylistOf(musicStyleDict[newDirection])
	
	#print("here we fade...")
	logging.info('Begin Fading...')
	
	if currentMusicChannel == "a":
		logging.info('Fading from A')
		currentMusicChannel = "b"
		#print "Switching to B channel"
		vola = maxMusicVolume
		volb = 0
		logging.info('Play and pause on B')
		musicChannelB = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		musicChannelB.pause()
		checkTheQueue()
		logging.info('Unpause B')
		musicChannelB.unpause()
		while vola > 0:
			logging.info('Fading')
			#print(vola)
			vola -= 0.01
			volb += 0.01
			logging.info('Setting Volumes')
			musicChannelA.set_volume(vola)
			musicChannelB.set_volume(volb)
			time.sleep(0.03)
		logging.info('Done with fading')
		musicChannelB.set_volume(maxMusicVolume)
	else:
		logging.info('Fading from B')
		currentMusicChannel = "a"
		#print "Switching to A channel"
		volb = maxMusicVolume
		vola = 0
		logging.info('Play and pause on A')
		musicChannelA = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		musicChannelA.pause()
		checkTheQueue()
		logging.info('Unpause A')
		musicChannelA.unpause()
		while volb > 0:
			logging.info('Fading')
			#print(volb)
			volb -= 0.01
			vola += 0.01
			logging.info('Setting Volumes')
			musicChannelB.set_volume(volb)
			musicChannelA.set_volume(vola)
			time.sleep(0.05)
		logging.info('Done with fading')
		musicChannelA.set_volume(maxMusicVolume)
	logging.info('Setting to a new Directory')
	currentMusicStyle = newDirection
	logging.info('All done with the fading')

def loadSoundEffects(directory):
	logging.info('Loading Soundeffects')
	global sfxDict
	#print("loading sfx for ")
	#print(directory)
	sfxDict = defaultdict(list)
	finaldir = "/home/pi/Raspberry-Pi-Audiomixer/sound/" + directory + "/sfx/"
	for item in glob.iglob(finaldir + "*"):
		item = item.replace(finaldir, "")
		#print(item)
		sfxDict[item[0]].append(item)
	logging.info('Done loading Soundeffects')

def checkTheQueue():
	logging.info('Checking the queue')
	global currentPlaylist
	global currentMusicStyle
	if currentMusicChannel == "a":
		logging.info('Checking A')
		if musicChannelA.get_queue() is None:
			logging.info('Nothing in the Queue of A')
			#print("queue empty!")
			if len(currentPlaylist) == 0:
				logging.info('Playist empty, making a new one')
				#print("playlist was empty, makin a new one")
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			logging.info('Setting a new song')
			musicChannelA.queue(pygame.mixer.Sound(currentPlaylist[0]))
			logging.info('Removing from playlist')
			currentPlaylist.remove(currentPlaylist[0])
			logging.info('Done')
			#print("done!")
	else:
		logging.info('Checking B')
		if musicChannelB.get_queue() is None:
			logging.info('Nothing in the Queue of B')
			#print("queue empty!")
			if len(currentPlaylist) == 0:
				logging.info('Playlist empty, making new one')
				#print("playlist was empty, makin a new one")
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			logging.info('Setting a new song')
			musicChannelB.queue(pygame.mixer.Sound(currentPlaylist[0]))
			logging.info('Removing from playlist')
			currentPlaylist.remove(currentPlaylist[0])
			logging.info('Done')
			#print("done!")

def playByKey(key):
	logging.info('Playing something because %s %s', key, ' was pressed')
	global sfxDict
	global musicStyleDict
	global currentMusicStyle
	if currentMusicStyle != "0":
		if key in sfxDict:
			logging.info('I have a sound for that!!)
			sfxToPlay = "/home/pi/Raspberry-Pi-Audiomixer/sound/" + musicStyleDict[currentMusicStyle] + "/sfx/" + random.choice(sfxDict[key])
			logging.info('Playing %s', sfxToPlay)
			#print("I'll play...")
			#print(sfxToPlay)
			pygame.mixer.Sound(sfxToPlay).play()
			logging.info('I played it, are ya happy?')
		else:
			pygame.mixer.Sound(warnSound).play()
			logging.info('I have nothing for %s', key)
			#print("I have nothing for this key...")
			#print(key)
	else:
		pygame.mixer.Sound(warnSound).play()
		logging.info('No music playing yet, no soundeffects for you')
		#print("No soundeffects before you switch to some music!")
		
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
				#print(vol)
				logging.info(vol)
				vol += 0.01
				musicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol < maxMusicVolume:
				#print(vol)
				logging.info(vol)
				vol += 0.01
				musicChannelB.set_volume(vol)
				time.sleep(0.03)
		logging.info('Setting the Volume at the end')
		#print("setting to" + str(maxMusicVolume))
		musicChannelA.set_volume(maxMusicVolume)
	else:
		logging.info('Volume is already at 100%')
		#print("Volume is already at 100%!")
		
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
				#print(vol)
				logging.info(vol)
				vol -= 0.01
				musicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol > maxMusicVolume:
				#print(vol)
				logging.info(vol)
				vol -= 0.01
				musicChannelB.set_volume(vol)
				time.sleep(0.03)
		logging.info('Setting Volume at the end')
		musicChannelA.set_volume(maxMusicVolume)
	else:
		logging.info('Volume is already at 100%')
		#print("Volume is already at 0%!")

logging.info('Startup Sound')
pygame.mixer.Sound('/home/pi/Raspberry-Pi-Audiomixer/startup-sound.ogg').play()
logging.info('Entering while loop')
while breaker:
	#activate toggle mode
	if keyboard.is_pressed('space'):
		#waiting for key to lift
		while keyboard.is_pressed('space'):
			pass
		logging.info('Space was pressed, waiting for a number to fade to other music')
		#print('Listening for fade....')
		#waiting for input to change the channel
		while True:
			if keyboard.is_pressed('1') and '1' in musicStyleDict:
				while keyboard.is_pressed('1'):
					pass
				logging.info('1')
				#print('1')
				fadeTo('1')
				break
			if keyboard.is_pressed('2') and '2' in musicStyleDict:
				while keyboard.is_pressed('2'):
					pass
				logging.info('2')
				#print('2')
				fadeTo('2')
				break
			if keyboard.is_pressed('3') and '3' in musicStyleDict:
				while keyboard.is_pressed('3'):
					pass
				logging.info('3')
				#print('3')
				fadeTo('3')
				break
			if keyboard.is_pressed('4') and '4' in musicStyleDict:
				while keyboard.is_pressed('4'):
					pass
				logging.info('4')
				#print('4')
				fadeTo('4')
				break
			if keyboard.is_pressed('5') and '5' in musicStyleDict:
				while keyboard.is_pressed('5'):
					pass
				logging.info('5')
				#print('5')
				fadeTo('5')
				break
			if keyboard.is_pressed('6') and '6' in musicStyleDict:
				while keyboard.is_pressed('6'):
					pass
				logging.info('6')
				#print('6')
				fadeTo('6')
				break
			if keyboard.is_pressed('7') and '7' in musicStyleDict:
				while keyboard.is_pressed('7'):
					pass
				logging.info('7')
				#print('7')
				fadeTo('7')
				break
			if keyboard.is_pressed('8') and '8' in musicStyleDict:
				while keyboard.is_pressed('8'):
					pass
				logging.info('8')
				#print('8')
				fadeTo('8')
				break
			if keyboard.is_pressed('9') and '9' in musicStyleDict:
				while keyboard.is_pressed('9'):
					pass
				logging.info('9')
				#print('9')
				fadeTo('9')
				break
			if keyboard.is_pressed('0') and '0' in musicStyleDict:
				while keyboard.is_pressed('0'):
					pass
				logging.info('0')
				#print('0')
				fadeTo('0')
				break		
			if keyboard.is_pressed('space'):
				while keyboard.is_pressed('space'):
					pass
				logging.info('Alright, we are not fading then.')
				#print('No more fading then...')
				break
	if keyboard.is_pressed('1'):
		while keyboard.is_pressed('1'):
			pass
		logging.info('SFX key 1')
		#print('SFX1')
		playByKey('1')
	if keyboard.is_pressed('2'):
		while keyboard.is_pressed('2'):
			pass
		logging.info('SFX key 2')
		#print('SFX2')
		playByKey('2')
	if keyboard.is_pressed('3'):
		while keyboard.is_pressed('3'):
			pass
		logging.info('SFX key 3')
		#print('SFX3')
		playByKey('3')
	if keyboard.is_pressed('4'):
		while keyboard.is_pressed('4'):
			pass
		logging.info('SFX key 4')
		#print('SFX4')
		playByKey('4')
	if keyboard.is_pressed('5'):
		while keyboard.is_pressed('5'):
			pass
		logging.info('SFX key 5')
		#print('SFX5')
		playByKey('5')
	if keyboard.is_pressed('6'):
		while keyboard.is_pressed('6'):
			pass
		logging.info('SFX key 6')
		#print('SFX6')
		playByKey('6')
	if keyboard.is_pressed('7'):
		while keyboard.is_pressed('7'):
			pass
		logging.info('SFX key 7')
		#print('SFX7')
		playByKey('7')
	if keyboard.is_pressed('8'):
		while keyboard.is_pressed('8'):
			pass
		logging.info('SFX key 8')
		#print('SFX8')
		playByKey('8')
	if keyboard.is_pressed('9'):
		while keyboard.is_pressed('9'):
			pass
		logging.info('SFX key 9')
		#print('SFX9')
		playByKey('9')
	if keyboard.is_pressed('0'):
		while keyboard.is_pressed('0'):
			pass
		logging.info('SFX key 0')
		#print('SFX0')
		playByKey('0')
	if keyboard.is_pressed('+'):
		while keyboard.is_pressed('+'):
			pass
		logging.info('LOUDER')
		#print('LOUDER')
		turnMusicUp()
	if keyboard.is_pressed('-'):
		while keyboard.is_pressed('-'):
			pass
		logging.info('Shut up a litte?')
		#print('Shut up a little?')
		turnMusicDown()
	if keyboard.is_pressed('enter'):
		while keyboard.is_pressed('enter'):
			pass
		rlybreak = True
		logging.info('Enter was pressed. Really quit? Press Enter Again to quit')
		#print("Really quit? Enter to quit!")
		while rlybreak:
			if keyboard.is_pressed('enter'):
				logging.info('We are out then')
				#pygame.quit()
				breaker = False
				rlybreak = False
				break
			if keyboard.is_pressed('0'):
				while keyboard.is_pressed('0'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('1'):
				while keyboard.is_pressed('1'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('2'):
				while keyboard.is_pressed('2'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('3'):
				while keyboard.is_pressed('3'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('4'):
				while keyboard.is_pressed('4'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('5'):
				while keyboard.is_pressed('5'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('6'):
				while keyboard.is_pressed('6'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('7'):
				while keyboard.is_pressed('7'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('8'):
				while keyboard.is_pressed('8'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
				logging.info('Not quitting yet')
			if keyboard.is_pressed('9'):
				while keyboard.is_pressed('9'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('space'):
				while keyboard.is_pressed('space'):
					pass
				logging.info('Not quitting yet')
				#print("I'll break, then")
				rlybreak = False
				break


	else:
		pass
	