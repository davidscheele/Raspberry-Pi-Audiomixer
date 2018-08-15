import pygame, time, glob, random, os, keyboard
from random import randrange, sample
from collections import defaultdict

#os.environ["SDL_VIDEODRIVER"] = "dummy" # or maybe 'fbcon'

breaker = True

currentMusicStyle = "0"

def loadMusicStyles():	
	with open('/home/pi/Raspberry-Pi-Audiomixer/musicstyleorder') as file:
		musicStyleDict = {}
		counter = 1
		for line in file:
			if line[0] != "#":
				line = line.replace("\n", "")
				musicStyleDict[str(counter)] = line
				counter += 1
	print(musicStyleDict)
	return musicStyleDict

musicStyleDict = loadMusicStyles()
maxMusicVolume = 0.5

warnSound = "/home/pi/Raspberry-Pi-Audiomixer/warning.ogg"

pygame.init()
#pygame.display.set_caption('super-mc-audiomix')
pygame.mixer.init()
#os.putenv('SDL_VIDEODRIVER', 'fbcon')
pygame.display.init()
SCREEN = pygame.display.set_mode((1, 1))
currentMusicChannel = "a"
musicChannelA = pygame.mixer.Sound("/home/pi/Raspberry-Pi-Audiomixer/silence-1-second.wav").play()
musicChannelB = pygame.mixer.Sound("/home/pi/Raspberry-Pi-Audiomixer/silence-1-second.wav").play()
currentPlaylist = []
sfxDict = defaultdict(list)

def getRandomPlaylistOf(directory):
	finaldir = "/home/pi/Raspberry-Pi-Audiomixer/sound/" + directory + "/bgm/*"
	playlist = []
	for result in glob.iglob(finaldir):
		playlist.insert(randrange(len(playlist)+1), result)
	return playlist

def getNextSongFromPlaylist():
	global currentPlaylist
	chosenTitle = currentPlaylist[0]
	currentPlaylist.remove(currentPlaylist[0])
	return chosenTitle

def fadeTo(newDirection):
	global currentPlaylist
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	global currentMusicStyle
	
	print("getting all the stuff")
	
	loadSoundEffects(musicStyleDict[newDirection])
	currentPlaylist = getRandomPlaylistOf(musicStyleDict[newDirection])
	
	print("here we fade...")
	
	if currentMusicChannel == "a":
		currentMusicChannel = "b"
		print "Switching to B channel"
		vola = maxMusicVolume
		volb = 0
		musicChannelB = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		musicChannelB.pause()
		checkTheQueue()
		musicChannelB.unpause()
		while vola > 0:
			print(vola)
			vola -= 0.01
			volb += 0.01
			musicChannelA.set_volume(vola)
			musicChannelB.set_volume(volb)
			time.sleep(0.03)
		musicChannelB.set_volume(maxMusicVolume)
	else:
		currentMusicChannel = "a"
		print "Switching to A channel"
		volb = maxMusicVolume
		vola = 0
		musicChannelA = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		musicChannelA.pause()
		checkTheQueue()
		musicChannelA.unpause()
		while volb > 0:
			print(volb)
			volb -= 0.01
			vola += 0.01
			musicChannelB.set_volume(volb)
			musicChannelA.set_volume(vola)
			time.sleep(0.05)
		musicChannelA.set_volume(maxMusicVolume)
	currentMusicStyle = newDirection

def loadSoundEffects(directory):
	global sfxDict
	print("loading sfx for ")
	print(directory)
	sfxDict = defaultdict(list)
	finaldir = "/home/pi/Raspberry-Pi-Audiomixer/sound/" + directory + "/sfx/"
	for item in glob.iglob(finaldir + "*"):
		item = item.replace(finaldir, "")
		print(item)
		sfxDict[item[0]].append(item)

def checkTheQueue():
	global currentPlaylist
	global currentMusicStyle
	if currentMusicChannel == "a":
		if musicChannelA.get_queue() is None:
			print("queue empty!")
			if len(currentPlaylist) == 0:
				print("playlist was empty, makin a new one")
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			musicChannelA.queue(pygame.mixer.Sound(currentPlaylist[0]))
			currentPlaylist.remove(currentPlaylist[0])
			print("done!")
	else:
		if musicChannelB.get_queue() is None:
			print("queue empty!")
			if len(currentPlaylist) == 0:
				print("playlist was empty, makin a new one")
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			musicChannelB.queue(pygame.mixer.Sound(currentPlaylist[0]))
			currentPlaylist.remove(currentPlaylist[0])
			print("done!")

def playByKey(key):
	global sfxDict
	global musicStyleDict
	global currentMusicStyle
	if currentMusicStyle != "0":
		if key in sfxDict:
			sfxToPlay = "/home/pi/Raspberry-Pi-Audiomixer/sound/" + musicStyleDict[currentMusicStyle] + "/sfx/" + random.choice(sfxDict[key])
			print("I'll play...")
			print(sfxToPlay)
			pygame.mixer.Sound(sfxToPlay).play()
		else:
			pygame.mixer.Sound(warnSound).play()
			print("I have nothing for this key...")
			print(key)
	else:
		pygame.mixer.Sound(warnSound).play()
		print("No soundeffects before you switch to some music!")
		
def turnMusicUp():
	global maxMusicVolume
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	if maxMusicVolume < 0.99:
		vol = maxMusicVolume
		maxMusicVolume += 0.1		
		if currentMusicChannel == "a":
			while vol < maxMusicVolume:
				print(vol)
				vol += 0.01
				musicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol < maxMusicVolume:
				print(vol)
				vol += 0.01
				musicChannelB.set_volume(vol)
				time.sleep(0.03)
		print("setting to" + str(maxMusicVolume))
		musicChannelA.set_volume(maxMusicVolume)
	else:
		print("Volume is already at 100%!")
		
def turnMusicDown():
	global maxMusicVolume
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	if maxMusicVolume > 0.01:
		vol = maxMusicVolume
		maxMusicVolume -= 0.1		
		if currentMusicChannel == "a":
			while vol > maxMusicVolume:
				print(vol)
				vol -= 0.01
				musicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol > maxMusicVolume:
				print(vol)
				vol -= 0.01
				musicChannelB.set_volume(vol)
				time.sleep(0.03)
		musicChannelA.set_volume(maxMusicVolume)
	else:
		print("Volume is already at 0%!")

pygame.mixer.Sound('/home/pi/Raspberry-Pi-Audiomixer/startup-sound.ogg').play()
while breaker:
	#activate toggle mode
	if keyboard.is_pressed('space'):
		#waiting for key to lift
		while keyboard.is_pressed('space'):
			pass
		print('Listening for fade....')
		#waiting for input to change the channel
		while True:
			if keyboard.is_pressed('1') and '1' in musicStyleDict:
				while keyboard.is_pressed('1'):
					pass
				print('1')
				fadeTo('1')
				break
			if keyboard.is_pressed('2') and '2' in musicStyleDict:
				while keyboard.is_pressed('2'):
					pass
				print('2')
				fadeTo('2')
				break
			if keyboard.is_pressed('3') and '3' in musicStyleDict:
				while keyboard.is_pressed('3'):
					pass
				print('3')
				fadeTo('3')
				break
			if keyboard.is_pressed('4') and '4' in musicStyleDict:
				while keyboard.is_pressed('4'):
					pass
				print('4')
				fadeTo('4')
				break
			if keyboard.is_pressed('5') and '5' in musicStyleDict:
				while keyboard.is_pressed('5'):
					pass
				print('5')
				fadeTo('5')
				break
			if keyboard.is_pressed('6') and '6' in musicStyleDict:
				while keyboard.is_pressed('6'):
					pass
				print('6')
				fadeTo('6')
				break
			if keyboard.is_pressed('7') and '7' in musicStyleDict:
				while keyboard.is_pressed('7'):
					pass
				print('7')
				fadeTo('7')
				break
			if keyboard.is_pressed('8') and '8' in musicStyleDict:
				while keyboard.is_pressed('8'):
					pass
				print('8')
				fadeTo('8')
				break
			if keyboard.is_pressed('9') and '9' in musicStyleDict:
				while keyboard.is_pressed('9'):
					pass
				print('9')
				fadeTo('9')
				break
			if keyboard.is_pressed('0') and '0' in musicStyleDict:
				while keyboard.is_pressed('0'):
					pass
				print('0')
				fadeTo('0')
				break		
			if keyboard.is_pressed('space'):
				while keyboard.is_pressed('space'):
					pass
				print('No more fading then...')
				break
	if keyboard.is_pressed('1'):
		while keyboard.is_pressed('1'):
			pass
		print('SFX1')
		playByKey('1')
	if keyboard.is_pressed('2'):
		while keyboard.is_pressed('2'):
			pass
		print('SFX2')
		playByKey('2')
	if keyboard.is_pressed('3'):
		while keyboard.is_pressed('3'):
			pass
		print('SFX3')
		playByKey('3')
	if keyboard.is_pressed('4'):
		while keyboard.is_pressed('4'):
			pass
		print('SFX4')
		playByKey('4')
	if keyboard.is_pressed('5'):
		while keyboard.is_pressed('5'):
			pass
		print('SFX5')
		playByKey('5')
	if keyboard.is_pressed('6'):
		while keyboard.is_pressed('6'):
			pass
		print('SFX6')
		playByKey('6')
	if keyboard.is_pressed('7'):
		while keyboard.is_pressed('7'):
			pass
		print('SFX7')
		playByKey('7')
	if keyboard.is_pressed('8'):
		while keyboard.is_pressed('8'):
			pass
		print('SFX8')
		playByKey('8')
	if keyboard.is_pressed('9'):
		while keyboard.is_pressed('9'):
			pass
		print('SFX9')
		playByKey('9')
	if keyboard.is_pressed('0'):
		while keyboard.is_pressed('0'):
			pass
		print('SFX0')
		playByKey('0')
	if keyboard.is_pressed('+'):
		while keyboard.is_pressed('+'):
			pass
		print('LOUDER')
		turnMusicUp()
	if keyboard.is_pressed('-'):
		while keyboard.is_pressed('-'):
			pass
		print('Shut up a little?')
		turnMusicDown()
	if keyboard.is_pressed('enter'):
		while keyboard.is_pressed('enter'):
			pass
		rlybreak = True
		print("Really quit? Enter to quit!")
		while rlybreak:
			if keyboard.is_pressed('enter'):
				#pygame.quit()
				breaker = False
				rlybreak = False
				break
			if keyboard.is_pressed('0'):
				while keyboard.is_pressed('0'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('1'):
				while keyboard.is_pressed('1'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('2'):
				while keyboard.is_pressed('2'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('3'):
				while keyboard.is_pressed('3'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('4'):
				while keyboard.is_pressed('4'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('5'):
				while keyboard.is_pressed('5'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('6'):
				while keyboard.is_pressed('6'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('7'):
				while keyboard.is_pressed('7'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('8'):
				while keyboard.is_pressed('8'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('9'):
				while keyboard.is_pressed('9'):
					pass
				print("I'll break, then")
				rlybreak = False
				break
			if keyboard.is_pressed('space'):
				while keyboard.is_pressed('space'):
					pass
				print("I'll break, then")
				rlybreak = False
				break


	else:
		pass
	
	
	
	
	
#	os.system("wmctrl -a super-mc-audiomix")
#	for event in pygame.event.get():
#		if event.type == pygame.KEYDOWN:
#			if event.key == pygame.SPACE:
#				while true:
#				if pygame.key.name(event.key) in musicStyleDict:
#					fadeTo(pygame.key.name(event.key))
#			elif event.key == pygame.K_MINUS:
#				turnMusicDown()
#			elif event.key == pygame.K_PLUS:
#				turnMusicUp()
#			elif event.key == pygame.K_ESCAPE:
#				breaker = True
#				print("Really quit? Enter to quit!")
#				while breaker:
#					for event in pygame.event.get():
#						if event.type == pygame.KEYDOWN:
#							if event.key == pygame.K_RETURN:
#								pygame.quit()
#							else:
#								print("I'll break, then")
#								breaker = False
#								break
#			else:
#				playByKey(pygame.key.name(event.key))